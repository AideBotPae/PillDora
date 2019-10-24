# !/usr/bin/env
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
"""
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import json
import logging
import re

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.replykeyboardremove import ReplyKeyboardRemove

import botui.telegramcalendar
from server.serverworker import ServerWorker
from ..imagerecognition.ocr.ocr import TextRecognition

# LOG INFORMATION
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('AideBot')

# TOKENS FOR THE TELEGRAM BOT
TOKEN_AIDEBOT = '902984072:AAFd0KLLAinZIrGhQvVePQwBt3WJ1QQQDGs'
TOKEN_TEST = '877926240:AAEuBzlNaqYM_kXbOMxs9lzhFsR7UpoqKWQ'
TOKEN_PILLDORA = '938652990:AAETGF-Xh2_njSdCLn2KibcprZXH1hhqsiI'

# STATES OF THE APP
LOGIN, NEW_USER, CHOOSING, INTR_MEDICINE, CHECK_MED, GET_CN, CHECK_REM, JOURNEY, END = range(9)

# FUNCTIONS FOR COMMUNICATING WITH DATA BASE
QUERIES = ['CHECK USER', 'CHECK PASSWORD', 'NEW PASSWORD', 'INTRODUCE MEDICINE', 'TASKS CALENDAR', 'HISTORY', 'JOURNEY',
           'GET REMINDER', 'DELETE REMINDER']

# MANAGE WHOLE INFORMATION
aide_bot = {}

# TAGS TO MANAGE INTRODUCING MEDICINES
INTR_MEDICINE_MSSGS = ["What is the medicine's name (CN)?\n You can also send me a photo of the package!",
                       "How many pills are in the packaging?",
                       "How often do you take your pill (in hours)?",
                       "Which day does treatment end?", "When does the medicine expire?"]
MEDICINE_TAGS = ['NAME', 'QUANTITY', 'FREQUENCY', 'END_DATE', 'EXP_DATE']

# KEYBOARD AND MARKUPS
reply_keyboard = [[u'Introduce Medicine \U0001F48A', u'Calendar \U0001F4C6'],
                  [u'History \U0001F4D6', u'Delete reminder \U0001F514'], [u'Journey \U00002708', u'Exit \U0001F6AA']]
yes_no_reply_keyboard = [['YES', 'NO']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
yes_no_markup = ReplyKeyboardMarkup(yes_no_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


class PillDora:
    """
    Telegram bot that serves as an aide to the clients of the product. It has a set of features that help customers
    to remember to take their pills (how many and when) and manages the customer's receipts and meds provisions.
    """

    # GETTERS AND SETTERS TO EASY FUNCTIONS
    def set_state(self, user_id, state):
        aide_bot[user_id]['states'][1] = aide_bot[user_id]['states'][0]
        aide_bot[user_id]['states'][0] = state
        return state

    # Returns the state of the bot for a specific user_id

    def get_states(self, user_id):
        return aide_bot[user_id]['states']

    # Returns the last medicine associated for a specific user_id
    def get_medicine(self, user_id):
        return aide_bot[user_id]['medicine']

    # Insertion of a medicine for a specific user_id
    def set_medicine(self, user_id, num, text):
        aide_bot[user_id]['medicine'][MEDICINE_TAGS[num]] = text

    # Returns the dates on a journey for a specific user_id
    def get_dates(self, user_id):
        return aide_bot[user_id]['journey']

    # Insertion of the date of a journey depending on the text, it is the departure or return for a specific user_id
    def set_dates(self, user_id, text, date):
        if text == "departure":
            aide_bot[user_id]['journey'][0] = date
        else:
            aide_bot[user_id]['journey'][1] = date

    # Insertion of the number of medicines associated to a medicine for a specific user_id
    def set_counter(self, user_id, num):
        aide_bot[user_id]['intr_medicine_counter'] = num

    # Returns the number of medicines associated to a medicine for a specific user_id
    def get_counter(self, user_id):
        return aide_bot[user_id]['intr_medicine_counter']

    # Insertion of the query that the Client sends to the ServerWorker for a specific user_id
    def set_query(self, user_id, keys, values):
        # We use a dictionary for the parameters of the query on the JSON string
        parameters = {}
        for key in keys:
            parameters[key] = values[keys.index(key)]
        aide_bot[user_id]['query'] = parameters

    # Returns the query that that the Client sends to the ServerWorker for a specific user_id
    def get_query(self, user_id):
        return aide_bot[user_id]['query']

    # Insertion of the function that the bot is currently on for a specific user_id
    def set_function(self, user_id, text):
        aide_bot[user_id]['function'] = text

    # Returns the function that the bot is doing for a specific user_id
    def get_function(self, user_id):
        return aide_bot[user_id]['function']

    def send_query(self, user_id, query):
        """Sends the query to the ServerWorker and returns the JSON query response.

        :param user_id: User unique identifier (login)
        :param query: Query to be send to the ServerWorker
        :return: the response to the query from sever
        """
        return aide_bot[user_id]['serverworker'].handler_query(query)

    def create_query(self, user_id):
        """Creates a JSON from the parameters that we have introduced using the Getters and Setters

        :param user_id: User unique identifier (login)
        :return: query string generated
        """
        # We create a pseudo-class to have a template for the JSON
        query = {
            'user_id': user_id,
            'function': self.get_function(user_id),
            'parameters': self.get_query(user_id)
        }
        query = json.dumps(query)
        logger.info(query)
        return query

    def start(self, update, context):
        """Manages /start command initializing a new aide_bot dictionary for the new user. It also manaages a login.

        :param update: Updater for bot token
        :param context: Handler context
        :return: the new state to be on
        """
        user_id = update.message.from_user.id
        name = self.get_name(update.message.from_user)
        aide_bot[user_id] = {'states': [LOGIN, LOGIN], 'intr_medicine_counter': 0,
                             'medicine': {tag: '' for tag in MEDICINE_TAGS}, 'journey': ['None', 'None'],
                             'function': 'none', 'query': {}, 'serverworker': ServerWorker(user_id)}
        logger.info('User ' + name + ' has connected to AideBot: ID is ' + str(user_id))
        context.bot.send_message(chat_id=user_id, text=("Welcome " + name + " ! My name is AideBot"))

        if self.user_verification(user_id) == "True":
            update.message.reply_text("Enter your password in order to get Assistance:")
            return self.set_state(user_id, LOGIN)
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=("Welcome to the HealthCare Assistant AideBot!\n"
                                           "Enter new password for creating your account:"))
        return self.set_state(user_id, NEW_USER)

    def get_name(self, user):
        """Resolve message data to a readable name.

        :param user: User identifier
        :return: first name of the user
        """
        try:
            name = user.first_name
        except (NameError, AttributeError):
            logger.info("No username or first name.. wtf")
            return ""
        return name

    def user_verification(self, user_id):
        """Verification of the UserID, if he has account or if it is first visit in AideBot

        :param user_id: User unique identifier
        :return: a boolean indicating whether the user is registered or not
        """
        self.set_function(user_id, 'CHECK USER')
        self.set_query(user_id, ["user_id"], [str(user_id)])
        query = self.create_query(user_id)
        response = self.send_query(user_id, query)
        return json.loads(response)["parameters"]["boolean"]

    def pwd_verification(self, password, user_id):
        """ Verification of the password for a UserID in DataBase

        :param password: Password introduced by the user
        :param user_id: User unique identifier
        :return: whether the password is the correct one or not
        """
        self.set_function(user_id, 'CHECK PASSWORD')
        self.set_query(user_id, ['password'], [password])
        query = self.create_query(user_id)
        response = self.send_query(user_id, query)
        return json.loads(response)["parameters"]["boolean"]

    @run_async
    def intr_pwd(self, update, context):
        """Method used to ask and introduce a password to check the identity of the user

        :param update: Updater for bot token
        :param context: Handler's context
        :return: the new state to be on (LOGIN if fails, CHOOSING if succeeds)
        """
        password = update.message.text
        logger.info('Password for user ' + self.get_name(update.message.from_user) + ' is ' + password)
        if self.pwd_verification(password, update.message.from_user.id) == "False":
            update.message.reply_text("Wrong Password. Enter correct password again:")
            return self.set_state(update.message.from_user.id, LOGIN)
        update.message.reply_text('Welcome ' + self.get_name(update.message.from_user) + '. How can I help you?',
                                  reply_markup=markup)
        return self.set_state(update.message.from_user.id, CHOOSING)

    @run_async
    def new_user(self, update, context):
        """ Function used to create user account --> associates a UserID with a new password

        :param update: Updater for bot token
        :param context: Handler's context
        :return: the new state to be on (NEW_USER if fails, CHOOSING if succeeds)
        """
        password = update.message.text
        logger.info('User introduced new password:  ' + password)
        user_id = update.message.from_user.id

        # Check for password difficulty:
        i = 0
        if re.search("[a-z]", password):
            i = i + 1
        if re.search("[0-9]", password):
            i = i + 1
        if re.search("[A-Z]", password):
            i = i + 1
        if re.search("[$#@]", password):
            i = i + 1
        if re.search("\s", password):
            i = 0
        if len(password) < 6 or len(password) > 12:
            i = 0

        if i > 2:
            update.message.reply_text("Valid Password")
            # Introduce new UserID-Password to DataBase
            self.set_function(user_id, 'NEW PASSWORD')
            self.set_query(user_id, ["new_password"], [password])
            query = self.create_query(user_id)
            self.send_query(user_id, query)
            update.message.reply_text('Welcome ' + self.get_name(update.message.from_user) + '. How can I help you?',
                                      reply_markup=markup)
            return self.set_state(update.message.from_user.id, CHOOSING)

        update.message.reply_text(
            "Not a Valid Password. Enter Password with 6 to 12 characters and minimum 3 of these types of characters: "
            "uppercase, lowercase, number and $, # or @")
        return self.set_state(update.message.from_user.id, NEW_USER)

    def manage_response(self, update, context):
        """Sends a query and gets the response, deciding what to do depending on the response 'function' field

        :param update: Updater for bot token
        :param context: Handler's context
        :return: state CHOOSING
        """
        user_id = update.message.from_user.id
        if (self.get_query(user_id) != "None") and (self.get_query(user_id) != {"None": "None"}):
            query = self.create_query(user_id)
            response = json.loads(self.send_query(user_id, query))
            if response['function'] == 'INTRODUCE MEDICINE':
                if response['parameters']["Code"] == "0":
                    logger.info("Medicine correctly introduced")
                elif response['parameters']["Code"] == "1":
                    logger.info("Medicine already in the database with different frequencies. PROBLEM")
                elif response['parameters']["Code"] == "2":
                    logger.info("Medicine already in the database with same frequencies. NO PROBLEM")
            if response['function'] == "DELETE REMINDER":
                if response['parameters']:
                    logger.info("Medicine correctly deleted")
                else:
                    logger.info("Medicine not deleted as did not exist in the database")
                    update.message.reply_text("Medicine introduced did not exist in your history.")
                    self.delete_reminder()
                    return self.set_state(update.message.from_user.id, CHOOSING)
            if response['function'] == "JOURNEY":
                logger.info("Medicines to take during journey correctly retrieved")
                update.message.reply_text(
                    "Medicines to take during journey:\n" + response['parameters']["journey_info"])

        self.set_query(user_id, ["None"], ["None"])
        self.set_function(user_id, "None")
        logger.info('User ' + self.get_name(update.message.from_user) + ' in the menu')
        update.message.reply_text("Is there any other way I can help you?", reply_markup=markup)
        return self.set_state(update.message.from_user.id, CHOOSING)

    @run_async
    def intr_medicine(self, update, context):
        """ Method that gets a new medicine to the recipes and starts the form

        :param update: Updater for bot token
        :param context: Handler's context
        :return: new state INTR_MEDICINE
        """
        logger.info('User introducing new medicine')
        update.message.reply_text(INTR_MEDICINE_MSSGS[self.get_counter(update.message.from_user.id)])
        return self.set_state(update.message.from_user.id, INTR_MEDICINE)

    def send_new_medicine(self, update, context):
        """Asks the user information in order to complete the medicine form, and once completed sets the query ready to
        be sent.

        :param update: Updater for bot token
        :param context: Handler's context
        :return: state INTR_MEDICINE while form not completed, state CHECK_MED once completed
        """
        try:
            user_id = update.message.from_user.id
            if self.get_counter(user_id) == 0:  # If we are in the first field of the form
                if update.message.photo:  # If user sent a photo, we apply
                    medicine_cn, validation_num = self.handle_pic(update, context, user_id)
                else:
                    medicine_cn, validation_num = self.split_code(update.message.text)

                if "error" in [medicine_cn, validation_num] or not self.verify_code(medicine_cn, validation_num):
                    update.message.reply_text(
                        "An error has occurred, please repeat the photo or manually introduce the CN")
                    return INTR_MEDICINE
                else:
                    self.set_medicine(user_id, self.get_counter(user_id), medicine_cn)
            else:
                self.set_medicine(user_id, self.get_counter(user_id), update.message.text)
        except:
            user_id = update.callback_query.from_user.id

        self.set_counter(user_id, self.get_counter(user_id) + 1)
        logger.info(self.get_medicine(user_id))
        if self.get_counter(user_id) != len(INTR_MEDICINE_MSSGS):
            if (self.get_counter(user_id) < 3):
                update.message.reply_text(INTR_MEDICINE_MSSGS[self.get_counter(user_id)])
                return INTR_MEDICINE
            else:
                context.bot.send_message(chat_id=user_id,
                                         text=INTR_MEDICINE_MSSGS[self.get_counter(user_id)],
                                         reply_markup=telegramcalendar.create_calendar())
                return CHECK_MED
        else:
            self.set_counter(user_id, 0)
            context.bot.send_message(chat_id=user_id,
                                     text='Is the medicine correctly introduced? ', reply_markup=yes_no_markup)
            context.bot.send_message(chat_id=user_id,
                                     text=self.show_medicine(user_id))
            self.set_query(user_id, list(self.get_medicine(user_id).keys()), list(self.get_medicine(user_id).values()))
            self.set_function(user_id, 'INTRODUCE MEDICINE')
            return self.set_state(user_id, CHECK_MED)

    def handle_pic(self, update, context, user_id):  # pic to obtain CN when send_new_medicine
        file = context.bot.getFile(update.message.photo[-1].file_id)
        filename = f'/home/paesav/Imágenes/{user_id}.jpg'
        file.download(filename)
        medicine_cn, validation_number = self.medicine_search(filename)
        print('\n', medicine_cn, validation_number, '\n')
        return medicine_cn, validation_number

    def medicine_search(self, filename):
        number, validation_number = TextRecognition().init(filename,
                                                            "/home/paesav/PAET2019/PillDora/imagetextrecognition/frozen_east_text_detection.pb")
        return number, validation_number

    def split_code(self, cn):
        if '.' in cn:
            return cn.split('.')[0], cn.split('.')[-1]
        elif len(cn) == 7:
            return cn[:6], cn[6]
        else:
            return 'error', 'error'

    def verify_code(self, medicine, validation_number):
        sum1 = 3 * (int(medicine[1]) + int(medicine[3]) + int(medicine[5]))
        sum2 = int(medicine[0]) + int(medicine[2]) + int(medicine[4])
        sum3 = sum1 + sum2 + 27
        res = 10 - (sum3 % 10)
        return res == int(validation_number)

    def obtain_medicine_name(self, CN):
        r = requests.get(url="https://cima.aemps.es/cima/rest/medicamento?cn=" + CN)
        data = r.json()
        namestring = data['presentaciones'][0]['nombre']
        return namestring

    def show_medicine(self, user_id):
        '''medicine_string = ''
        for tag in MEDICINE_TAGS:
            if tag == 'NAME':
                medicine_string += tag + ': ' + self.obtain_medicine_name(self.get_medicine(user_id)[tag]).split(' ')[
                    0] + '\n'
            else:
                medicine_string += tag + ': ' + self.get_medicine(user_id)[tag] + '\n'
        '''
        med_param = lambda x: self.obtain_medicine_name(self.get_medicine(user_id)[x]).split(' ')[0] if x == 'NAME' else self.get_medicine(user_id)[x]
        return '\n'.join(f'{tag}: {med_param(tag)}' for tag in MEDICINE_TAGS)

    @run_async
    def see_calendar(self, update, context):
        logger.info('User ' + self.get_name(update.message.from_user) + '  seeing calendar')
        update.message.reply_text("Please select a date: ",
                                  reply_markup=telegramcalendar.create_calendar())

    @run_async
    # Method that handles the situations and depending on the current state, changes the state
    def inline_handler(self, update, context):
        selected, date = telegramcalendar.process_calendar_selection(context.bot, update)
        user_id = update.callback_query.from_user.id
        if selected:
            if self.get_states(user_id)[0] == CHOOSING:
                context.bot.send_message(chat_id=user_id,
                                         text="You selected %s" % (date.strftime("%Y-%m-%d")),
                                         reply_markup=ReplyKeyboardRemove())
            if self.get_states(user_id)[0] == CHOOSING:
                self.get_calendar_tasks(update, context, date.strftime("%Y-%m-%d"), user_id)
                self.set_state(user_id, CHOOSING)
            elif self.get_states(user_id)[0] == JOURNEY:
                self.set_journey(update, context, date.strftime("%Y-%m-%d"))
                if self.get_states(user_id)[1] == CHOOSING:
                    self.set_state(user_id, JOURNEY)
                elif self.get_states(user_id)[1] == JOURNEY:
                    self.set_state(user_id, JOURNEY)
            elif self.get_states(user_id)[0] == INTR_MEDICINE:
                context.bot.send_message(chat_id=user_id,
                                         text=date.strftime("%Y-%m-%d"),
                                         reply_markup=ReplyKeyboardRemove())
                self.set_medicine(user_id, self.get_counter(user_id), date.strftime("%Y-%m-%d"))
                self.send_new_medicine(update, context)

    @run_async
    # Returns all the reminders associated for a specific date and user_id
    def get_calendar_tasks(self, update, context, date, user_id):
        logger.info('Tasks for the user on the date ' + date)
        # connects to DataBase with Date and UserId asking for all the tasks of this date
        self.set_function(user_id, "TASKS CALENDAR")
        self.set_query(user_id, ["date"], [date])
        query = self.create_query(user_id)
        response = json.loads(self.send_query(user_id, query))
        context.bot.send_message(chat_id=user_id,
                                 text="Reminders for " + date + " :\n")
        context.bot.send_message(chat_id=user_id, text=response['parameters']['tasks'])
        context.bot.send_message(chat_id=user_id, text="Is there any other way I can help you?",
                                 reply_markup=markup)

    @run_async
    # Method that prints systematically the history for a certain user_id
    def see_history(self, update, context):
        logger.info('User ' + self.get_name(update.message.from_user) + ' seeing history')
        # connects to DataBase with UserId asking for all the medications he is currently taking
        user_id = update.message.from_user.id
        self.set_function(user_id, "HISTORY")
        self.set_query(user_id, ["user_id"], [str(user_id)])
        query = self.create_query(user_id)
        response = json.loads(self.send_query(user_id, query))
        update.message.reply_text(
            "To sum up, you are currently taking these meds:\n" + response['parameters']['reminder_info'])
        self.set_query(user_id, ["None"], ["None"])
        return self.manage_response(update, context)

    @run_async
    # Deletes a reminder using a CN for a certain user_id
    def delete_reminder(self, update, context):
        logger.info('User ' + self.get_name(update.message.from_user) + ' deleting reminder')
        update.message.reply_text('Please Introduce CN of the Medicine you want to delete the reminder:')
        return self.set_state(update.message.from_user.id, GET_CN)

    # Method that asks for a CN and prints all the information and asks about if it should be removed or not
    def get_medicine_CN(self, update, context):
        medicine_CN = update.message.text
        user_id = update.message.from_user.id
        # connects to DataBase with UserId and get the current reminder for this medicine_CN.
        self.set_function(user_id, "GET REMINDER")
        self.set_query(user_id, ["CN"], [medicine_CN])
        query = self.create_query(user_id)
        response = json.loads(self.send_query(user_id, query))
        reminder_info = response['parameters']
        if reminder_info['CN'] == "False":
            update.message.reply_text('CN introduced is wrong, there is not any med with this CN')
            update.message.reply_text("Is there any other way I can help you?", reply_markup=markup)
            return self.set_state(user_id, CHOOSING)
        reminder_info = "Medicine " + response['parameters']['CN'] + " taken with a frequency of " + \
                        response['parameters'][
                            'frequency'] + " hours until the date of " + response['parameters']['end_date'] + "."
        update.message.reply_text('Reminder asked to be removed:\n ->\t' + reminder_info)
        update.message.reply_text('Is this the reminder you want to remove? ', reply_markup=yes_no_markup)
        self.set_query(user_id, ["CN"], [response['parameters']['CN']])
        self.set_function(user_id, 'DELETE REMINDER')
        return self.set_state(user_id, CHECK_REM)

    # Method that creates a journey to be handled later and asks for the information
    @run_async
    def create_journey(self, update, context):
        boolean = self.get_states(update.message.from_user.id)[0] == CHOOSING
        self.set_state(update.message.from_user.id, CHOOSING)
        logger.info('User ' + self.get_name(update.message.from_user) + ' creating journey')
        self.set_state(update.message.from_user.id, JOURNEY)
        if boolean:
            update.message.reply_text("Wow fantastic! So you are going on a trip...\nWhen are you leaving?",
                                      reply_markup=telegramcalendar.create_calendar())
        else:
            update.message.reply_text("No worries. Introduce right departure date:",
                                      reply_markup=telegramcalendar.create_calendar())
        return JOURNEY

    # Method that asks for the dates needed for a journey and changes the state of the bot to JOURNEY

    def set_journey(self, update, context, date):
        user_id = update.callback_query.from_user.id
        if self.get_states(user_id)[1] == CHOOSING:
            logger.info("Department date " + date)
            self.set_dates(user_id, "departure", date)
            context.bot.send_message(chat_id=user_id,
                                     text="Alright. I see you are leaving on " + date + ".\nWhen will you come back?",
                                     reply_markup=telegramcalendar.create_calendar())

        if self.get_states(user_id)[1] == JOURNEY:
            logger.info("Arrival date " + date)
            self.set_dates(user_id, "arrival", date)
            context.bot.send_message(chat_id=user_id,
                                     text="The arrival Date is on " + date + "\nIs this information correct?",
                                     reply_markup=yes_no_markup)
            self.set_query(user_id, ["departure_date", "arrival_date"],
                           [self.get_dates(user_id)[0], self.get_dates(user_id)[1]])
            self.set_function(user_id, 'JOURNEY')

    # Ends the communication between the user and the bot

    def exit(self, update, context):
        update.message.reply_text("See you next time")
        logger.info('User ' + self.get_name(update.message.from_user) + ' finish with AideBot')
        return END

    # Main of the Client.py, where the bot is activated and creates the transition to the different functionalities

    def main(self):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        updater = Updater(token=TOKEN_AIDEBOT, use_context=True, workers=50)
        dp = updater.dispatcher
        conv_handler = ConversationHandler(
            allow_reentry=True,
            entry_points=[CommandHandler('start', self.start)],

            states={
                LOGIN: [MessageHandler(Filters.text, self.intr_pwd)],
                NEW_USER: [MessageHandler(Filters.text, self.new_user)],
                CHOOSING: [MessageHandler(Filters.regex('^Introduce Medicine'),
                                          self.intr_medicine),
                           MessageHandler(Filters.regex('^Calendar'),
                                          self.see_calendar),
                           MessageHandler(Filters.regex('^History'),
                                          self.see_history),
                           MessageHandler(Filters.regex('^Delete reminder'),
                                          self.delete_reminder),
                           MessageHandler(Filters.regex('^Journey'),
                                          self.create_journey),
                           MessageHandler(Filters.regex('^Exit'), exit)
                           ],
                INTR_MEDICINE: [MessageHandler(Filters.text | Filters.photo, self.send_new_medicine)],
                CHECK_MED: [MessageHandler(Filters.regex('^YES$'), self.manage_response),
                            MessageHandler(Filters.regex('^NO$'), self.intr_medicine)
                            ],
                CHECK_REM: [MessageHandler(Filters.regex('^YES$'), self.manage_response),
                            MessageHandler(Filters.regex('^NO$'), self.delete_reminder)
                            ],
                GET_CN: [MessageHandler(Filters.text, self.get_medicine_CN)],
                JOURNEY: [MessageHandler(Filters.regex('^YES$'), self.manage_response),
                          MessageHandler(Filters.regex('^NO$'), self.create_journey)
                          ]
            },
            fallbacks=[MessageHandler(Filters.regex('^Exit$'), exit)]
        )

        dp.add_handler(conv_handler)
        dp.add_handler(CallbackQueryHandler(self.inline_handler))
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    pilldora = PillDora()
    pilldora.main()