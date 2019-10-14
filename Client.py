#!/usr/bin/env
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

"""
import json
import logging
import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, \
    CallbackQueryHandler
from telegram.ext.dispatcher import run_async

import telegramcalendar
from text_recognition_class import Text_Recognition

# LOG INFORMATION
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('AideBot')

# TOKENS FOR THE TELEGRAM BOT
TOKEN_AIDEBOT = '902984072:AAFd0KLLAinZIrGhQvVePQwBt3WJ1QQQDGs'
TOKEN_PROVE = '877926240:AAEuBzlNaqYM_kXbOMxs9lzhFsR7UpoqKWQ'
TOKEN_PILLDORA = '938652990:AAETGF-Xh2_njSdCLn2KibcprZXH1hhqsiI'

# STATES OF THE APP
LOGIN, NEW_USER, CHOOSING, INTR_MEDICINE, CHECK_MED, GET_CN, CHECK_REM, JOURNEY, END = range(9)

# FUNCTIONS FOR COMMUNICATING WITH DATA BASE
QUERIES = ['CHECK USER', 'CHECK PASSWORD', 'NEW PASSWORD', 'INTRODUCE MEDICINE', 'TASKS CALENDAR', 'HISTORY', 'JOURNEY',
           'GET REMINDER', 'DELETE REMINDER']
# MANAGE WHOLE INFORMATION
aide_bot = {}

# TAGS TO MANAGE INTRODUCING MEDICINES
INTR_MEDICINE_MSSGS = ["What is the medicine's name (CN)?", "How many pills are in the packaging?",
                       "How often do you take your pill (in hours)?",
                       "Which day does treatment end?", "When does the medicine expire?"]
MEDICINE_TAGS = ['NAME', 'QUANTITY', 'FREQUENCY', 'END_DATE', 'EXP_DATE']

# KEYBOARD AND MARKUPS
reply_keyboard = [['Introduce Medicine'+u'U\00002708', 'Calendar'+u'U\0001F4C6'], ['History'+u'U\0001F4DG', 'Delete reminder'+'U\0001F514'], ['Journey'+u'U\00002708', 'Exit'+u'U\0001F6AA']]
yes_no_reply_keyboard = [['YES', 'NO']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
yes_no_markup = ReplyKeyboardMarkup(yes_no_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


# GETTERS AND SETTERS TO EASY FUNCTIONS
def set_state(user_id, state):
    aide_bot[user_id]['states'][1] = aide_bot[user_id]['states'][0]
    aide_bot[user_id]['states'][0] = state
    return state


def get_states(user_id):
    return aide_bot[user_id]['states']


def get_medicine(user_id):
    return aide_bot[user_id]['medicine']


def set_medicine(user_id, num, text):
    aide_bot[user_id]['medicine'][MEDICINE_TAGS[num]] = text


def get_dates(user_id):
    return aide_bot[user_id]['journey']


def set_dates(user_id, text, date):
    if (text == "departure"):
        aide_bot[user_id]['journey'][0] = date
    else:
        aide_bot[user_id]['journey'][1] = date


def set_counter(user_id, num):
    aide_bot[user_id]['intr_medicine_counter'] = num


def get_counter(user_id):
    return aide_bot[user_id]['intr_medicine_counter']


def set_query(user_id, text):
    aide_bot[user_id]['query'] = text


def get_query(user_id):
    return aide_bot[user_id]['query']


def set_function(user_id, text):
    aide_bot[user_id]['function'] = text


def get_function(user_id):
    return aide_bot[user_id]['function']


def create_query(user_id):
    query = {
        'user_id': user_id,
        'function': get_function(user_id),
        'parameters': get_query(user_id)
    }
    query = json.dumps(query)
    logger.info(query)
    return query


# MANAGE "/START" COMMAND ON TELEGRAM INPUT
def start(update, context):
    user_id = update.message.from_user.id
    name = get_name(update.message.from_user)
    aide_bot[user_id] = {'states': [LOGIN, LOGIN], 'intr_medicine_counter': 0,
                         'medicine': {tag: '' for tag in MEDICINE_TAGS}, 'journey': ['None', 'None'],
                         'function': 'none', 'query': "none"}
    logger.info('User ' + name + ' has connected to AideBot: ID is ' + str(user_id))
    context.bot.send_message(chat_id=user_id, text=("Welcome " + name + " ! My name is AideBot"))

    if (user_verification(user_id)):
        update.message.reply_text("Enter your password in order to get Assistance:")
        return set_state(user_id, LOGIN)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=("Welcome to the HealthCare Assistant AideBot."
                                                                       "Enter new password for creating your account:"))
    return set_state(user_id, NEW_USER)


# Resolve message data to a readable name
def get_name(user):
    try:
        name = user.first_name
    except (NameError, AttributeError):
        try:
            name = user.username
        except (NameError, AttributeError):
            logger.info("No username or first name.. wtf")
            return ""
    return name


# Verificates is UserID has account or it is first visit in AideBot
def user_verification(user_id):
    set_function(user_id, 'CHECK USER')
    set_query(user_id, ['user_id : ' + str(user_id)])
    query = create_query(user_id)
    return True


# Verificates password for UserID in DataBase
def pwd_verification(password, user_id):
    set_function(user_id, 'CHECK PASSWORD')
    set_query(user_id, ['password : ' + password])
    query = create_query(user_id)
    return True


# function used to Introduce Password
@run_async
def intr_pwd(update, context):
    password = update.message.text
    logger.info('Password for user ' + get_name(update.message.from_user) + ' is ' + password)
    if (pwd_verification(password, update.message.from_user.id) == False):
        update.message.reply_text("Wrong Password. Enter correct password again:")
        return set_state(update.message.from_user.id, LOGIN)
    update.message.reply_text('Welcome ' + get_name(update.message.from_user) + '. How can I help you?',
                              reply_markup=markup)
    return set_state(update.message.from_user.id, CHOOSING)


# function used to create user account --> associate UserID with Pwd
@run_async
def new_user(update, context):
    password = update.message.text
    logger.info('User introduce new password:  ' + password)
    user_id = update.message.from_user.id

    # check for password difficulty.
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
    if (len(password) < 6 or len(password) > 12):
        i = 0

    if (i > 2):
        update.message.reply_text("Valid Password")
        # Introduce new UserID-Password to DataBase
        set_function(user_id, 'NEW PASSWORD')
        set_query(['new_password : ' + password])
        query = create_query(user_id)
        update.message.reply_text('Welcome ' + get_name(update.message.from_user) + '. How can I help you?',
                                  reply_markup=markup)
        return set_state(update.message.from_user.id, CHOOSING)

    update.message.reply_text(
        "Not a Valid Password. Enter Password with 6 to 12 characters and minimum 3 of these types of characters: uppercase, lowercase, number and $, # or @")
    return set_state(update.message.from_user.id, NEW_USER)


def choose_function(update, context):
    user_id = update.message.from_user.id
    if (get_query(user_id) != "None"):
        query = create_query(user_id)

    set_query(user_id, "None")
    set_function(user_id, "None")
    logger.info('User ' + get_name(update.message.from_user) + ' in the menu')
    update.message.reply_text("Is there any other way I can help you?", reply_markup=markup)
    return set_state(update.message.from_user.id, CHOOSING)


@run_async
def intr_medicine(update, context):
    logger.info('User introducing new medicine')
    update.message.reply_text(INTR_MEDICINE_MSSGS[get_counter(update.message.from_user.id)])
    return set_state(update.message.from_user.id, INTR_MEDICINE)


def handle_pic(update, context, user_id):  # pic to obtain CN when send_new_medicine
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download(f'/home/paesav/Imágenes/{user_id}.jpg')
    medicine_cn, validation_number = medicine_search(f"{user_id}.jpg")

    return medicine_cn, validation_number


def medicine_search(filename):
    number, validation_number = Text_Recognition().init(filename, "frozen_east_text_detection.pb")

    return number, validation_number


def split_code(cn):
    if '.' in cn:
        return cn.split('.')[0], cn.split('.')[-1]
    elif len(cn) == 7:
        return cn[:6], cn[6]
    else:
        return 'error', 'error'


def verify_code(medicine, validation_number):
    sum1 = 3 * (int(medicine[1]) + int(medicine[3]) + int(medicine[5]))
    sum2 = int(medicine[0]) + int(medicine[2]) + int(medicine[4])
    sum3 = sum1 + sum2 + 27
    res = 10 - (sum3 % 10)
    return res == int(validation_number)


def send_new_medicine(update, context):
    try:
        user_id = update.message.from_user.id
        if get_counter(user_id) == 0:
            if update.message.photo:
                medicine_cn, validation_num = handle_pic(update, context, user_id)
            else:
                medicine_cn, validation_num = split_code(update.message.text)

            if "error" in [medicine_cn, validation_num] or verify_code(medicine_cn, validation_num):
                context.message.reply_text(
                    "An error has occurred, please repeat the photo or manually introduce the CN")
                return INTR_MEDICINE
            else:
                set_medicine(user_id, get_counter(user_id), medicine_cn)
        else:
            set_medicine(user_id, get_counter(user_id), update.message.text)
    except:
        user_id = update.callback_query.from_user.id

    set_counter(user_id, get_counter(user_id) + 1)
    logger.info(get_medicine(user_id))
    if get_counter(user_id) != len(INTR_MEDICINE_MSSGS):
        if (get_counter(user_id) < 3):
            update.message.reply_text(INTR_MEDICINE_MSSGS[get_counter(user_id)])
            return INTR_MEDICINE
        else:
            context.bot.send_message(chat_id=user_id,
                                     text=INTR_MEDICINE_MSSGS[get_counter(user_id)],
                                     reply_markup=telegramcalendar.create_calendar())
            return CHECK_MED
    else:
        set_counter(user_id, 0)
        context.bot.send_message(chat_id=user_id,
                                 text='Is the medicine correctly introduced? ', reply_markup=yes_no_markup)
        context.bot.send_message(chat_id=user_id,
                                 text=show_medicine(user_id))
        set_query(user_id, str.replace(str.replace(show_medicine(user_id), "{", "["), "}", "]"))
        set_function(user_id, 'INTRODUCE MEDICINE')

        return set_state(user_id, CHECK_MED)


def show_medicine(user_id):
    medicine_string = ''
    for tag in MEDICINE_TAGS:
        medicine_string += tag + ': ' + get_medicine(user_id)[tag] + '\n'
    return medicine_string


@run_async
def see_calendar(update, context):
    logger.info('User ' + get_name(update.message.from_user) + '  seeing calendar')
    update.message.reply_text("Please select a date: ",
                              reply_markup=telegramcalendar.create_calendar())


@run_async
def inline_handler(update, context):
    selected, date = telegramcalendar.process_calendar_selection(context.bot, update)
    user_id = update.callback_query.from_user.id
    if selected:
        if (get_states(user_id)[0] == CHOOSING):
            context.bot.send_message(chat_id=user_id,
                                     text="You selected %s" % (date.strftime("%d/%m/%Y")),
                                     reply_markup=ReplyKeyboardRemove())
        if (get_states(user_id)[0] == CHOOSING):
            get_calendar_tasks(update, context, date.strftime("%d/%m/%Y"), user_id)
            set_state(user_id, CHOOSING)
        elif (get_states(user_id)[0] == JOURNEY):
            set_journey(update, context, date.strftime("%d/%m/%Y"))
            if (get_states(user_id)[1] == CHOOSING):
                set_state(user_id, JOURNEY)
            elif (get_states(user_id)[1] == JOURNEY):
                set_state(user_id, JOURNEY)
        elif (get_states(user_id)[0] == INTR_MEDICINE):
            context.bot.send_message(chat_id=user_id,
                                     text=date.strftime("%d/%m/%Y"),
                                     reply_markup=ReplyKeyboardRemove())
            set_medicine(user_id, get_counter(user_id), date.strftime("%d/%m/%Y"))
            send_new_medicine(update, context)


@run_async
def get_calendar_tasks(update, context, date, user_id):
    logger.info('Tasks for the user on the date ' + date)
    # connects to DataBase with Date and UserId asking for all the tasks of this date
    set_function(user_id, "TASKS CALENDAR")
    set_query(user_id, "[ date : " + date + "]")
    query = create_query(user_id)
    context.bot.send_message(chat_id=update.callback_query.from_user.id, text="Is there any other way I can help you?",
                             reply_markup=markup)


@run_async
def see_history(update, context):
    logger.info('User ' + get_name(update.message.from_user) + ' seeing history')
    # connects to DataBase with UserId asking for all the meds currently taking
    user_id = update.message.from_user.id
    set_function(user_id, "HISTORY")
    set_query(user_id, "[ user_id : " + str(user_id) + "]")
    query = create_query(user_id)

    set_query(user_id, 'None')
    return choose_function(update, context)


@run_async
def delete_reminder(update, context):
    logger.info('User ' + get_name(update.message.from_user) + ' deleting reminder')
    update.message.reply_text('Please Introduce CN of the Medicine you want to delete the reminder:')
    return set_state(update.message.from_user.id, GET_CN)


def get_medicine_CN(update, context):
    medicine_CN = update.message.text
    user_id = update.message.from_user.id
    # connects to DataBase with UserId and get the current reminder for this medicine_CN.
    set_function(user_id, "GET REMINDER")
    set_query(user_id, "[CN : " + medicine_CN + "]")
    query = create_query(user_id)
    reminder = 'Hola'

    update.message.reply_text('Reminder asked to be removed:\n\tMedicine: \n\tTaken from:\n\tEnd date:\n\tFrequency: ')
    update.message.reply_text('Is this the reminder you want to remove? ', reply_markup=yes_no_markup)
    set_query(user_id, reminder)
    set_function(user_id, 'DELETE REMINDER')
    return set_state(user_id, CHECK_REM)


@run_async
def create_journey(update, context):
    boolean = get_states(update.message.from_user.id)[0] == CHOOSING
    set_state(update.message.from_user.id, CHOOSING)
    logger.info('User ' + get_name(update.message.from_user) + ' creating journey')
    set_state(update.message.from_user.id, JOURNEY)
    if (boolean):
        update.message.reply_text("Wow fantastic! So you are going on a trip...\nWhen are you leaving?",
                                  reply_markup=telegramcalendar.create_calendar())
    else:
        update.message.reply_text("No worries. Introduce right departure date:",
                                  reply_markup=telegramcalendar.create_calendar())
    return JOURNEY


def set_journey(update, context, date):
    user_id = update.callback_query.from_user.id
    if (get_states(user_id)[1] == CHOOSING):
        logger.info("Department date " + date)
        set_dates(user_id, "departure", date)
        context.bot.send_message(chat_id=user_id,
                                 text="Alright. I see you are leaving on " + date + ".\nWhen will you come back?",
                                 reply_markup=telegramcalendar.create_calendar())

    if (get_states(user_id)[1] == JOURNEY):
        logger.info("Arrival date " + date)
        set_dates(user_id, "arrival", date)
        context.bot.send_message(chat_id=user_id,
                                 text="The arrival Date is on " + date + "\nIs this information correct?",
                                 reply_markup=yes_no_markup)
        set_query(user_id,
                  "[departure_date : " + get_dates(user_id)[0] + ", arrival date : " + get_dates(user_id)[1] + "]")
        set_function(user_id, 'JOURNEY')


def exit(update, context):
    update.message.reply_text("See you next time")
    logger.info('User ' + get_name(update.message.from_user) + ' finish with AideBot')
    return END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    updater = Updater(token=TOKEN_PILLDORA, use_context=True, workers=50)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[CommandHandler('start', start)],

        states={
            LOGIN: [MessageHandler(Filters.text, intr_pwd)],
            NEW_USER: [MessageHandler(Filters.text, new_user)],
            CHOOSING: [MessageHandler(Filters.regex('^Introduce Medicine$'),
                                      intr_medicine),
                       MessageHandler(Filters.regex('^Calendar$'),
                                      see_calendar),
                       MessageHandler(Filters.regex('^History$'),
                                      see_history),
                       MessageHandler(Filters.regex('^Delete reminder$'),
                                      delete_reminder),
                       MessageHandler(Filters.regex('^Journey$'),
                                      create_journey),
                       MessageHandler(Filters.regex('^Exit$'), exit)
                       ],
            INTR_MEDICINE: [MessageHandler(Filters.text | Filters.photo, send_new_medicine)],
            CHECK_MED: [MessageHandler(Filters.regex('^YES$'), choose_function),
                        MessageHandler(Filters.regex('^NO$'), intr_medicine)
                        ],
            CHECK_REM: [MessageHandler(Filters.regex('^YES$'), choose_function),
                        MessageHandler(Filters.regex('^NO$'), delete_reminder)
                        ],
            GET_CN: [MessageHandler(Filters.text, get_medicine_CN)],
            JOURNEY: [MessageHandler(Filters.regex('^YES$'), choose_function),
                      MessageHandler(Filters.regex('^NO$'), create_journey)
                      ]
        },
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), exit)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(inline_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
