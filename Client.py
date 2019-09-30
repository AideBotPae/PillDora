from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import requests
import re
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('AideBot')

TOKEN_AIDEBOT='902984072:AAFd0KLLAinZIrGhQvVePQwBt3WJ1QQQDGs'
TOKEN_PROVE= '877926240:AAEuBzlNaqYM_kXbOMxs9lzhFsR7UpoqKWQ'
LOGIN, NEW_USER, CHOOSING, INTR_MEDICINE = range(4)

reply_keyboard = [['Introduce Medicine', 'Calendar'],
                  ['History', 'Delete reminder'],
                  ['Journey' ,'Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

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


# Verificates password for UserID in DataBase
def pwd_verification(password):
    return True


# Verificates is UserID has account or it is first visit in AideBot
def user_verification(update, context):
    user_id = update.message.from_user.id
    return True


# function used to Introduce Password
def intr_pwd(update, context):
    password = update.message.text
    logger.info('Password is ' + password)
    if (pwd_verification(password) == False):
        update.message.reply_text("Wrong Password. Enter correct password again:")
        return LOGIN
    update.message.reply_text('Welcome ' + get_name(update.message.from_user) + '. How can I help you?', reply_markup=markup)
    return CHOOSING


# function used to create user account --> associate UserID with Pwd
def new_user(update, context):
    password = update.message.text
    # check if password difficulty.
    logger.info('New password is ' + password)
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
        i=0
    if (len(password) < 6 or len(password) > 12):
        i=0

    if (i > 2):
        update.message.reply_text("Valid Password")
        update.message.reply_text('Welcome ' + get_name(update.message.from_user) + '. How can I help you?',
                                  reply_markup=markup)
        # Introdue new UserID-Password to DataBase
        x = False
        return CHOOSING

    update.message.reply_text("Not a Valid Password. Enter Password with 6 to 12 characters and minimum 3 of these types of characters: uppercase, lowercase, number and $, # or @")
    return NEW_USER

def choose_function(update, context):
     return True


def start(update, context):
    logger.info('User has connected to AideBot: /start')
    user_id = update.message.from_user.id
    name = get_name(update.message.from_user)
    context.bot.send_message(chat_id=update.message.chat_id, text=("Welcome " + name + " ! My name is AideBot"))
    logger.info('Name of user is: ' + name + " and its ID is " + str(user_id))
    if (user_verification(update, context)):
        update.message.reply_text("Enter your password in order to get Assistance:")
        return LOGIN
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=("Welcome to the HealthCare Assistant AideBot."
                                                                       "Enter new password for creating your account:"))
    return NEW_USER


def intr_medicine(update, context):
   logger.info('User introducing new medicine')

   update.message.reply_text('Please Introduce New Medicine as Follows:')

   return INTR_MEDICINE

def see_calendar(update, context):
   logger.info('User seeing calendar')


   update.message.reply_text(' Can I help you more?',
                             reply_markup=markup)
   return CHOOSING

def see_history(update, context):
   logger.info('User seeing history')

   update.message.reply_text(' Can I help you more?',
                             reply_markup=markup)
   return CHOOSING

def delete_reminder(update, context):

   update.message.reply_text(' Can I help you more?',
                             reply_markup=markup)
   logger.info('User deleting reminder')
   return CHOOSING

def done(update, context):
   update.message.reply_text("See you next time")
   logger.info('User finish with AideBot')
   return ConversationHandler.END


def create_journey(update, context):
   update.message.reply_text(' Can I help you more?',
                             reply_markup=markup)
   logger.info('User creating journey')
   return CHOOSING


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    updater = Updater(token=TOKEN_PROVE, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LOGIN: [MessageHandler(Filters.text, intr_pwd)],
            NEW_USER: [MessageHandler(Filters.text, new_user)],
            CHOOSING: [MessageHandler(Filters.regex('^(Introduce Medicine)$'),
                                      intr_medicine),
                       MessageHandler(Filters.regex('^Calendar$'),
                                      see_calendar),
                       MessageHandler(Filters.regex('^History'),
                                      see_history),
                       MessageHandler(Filters.regex('^Delete reminder'),
                                      delete_reminder),
                       MessageHandler(Filters.regex('^Journey'),
                                      create_journey),
                       ],
            INTR_MEDICINE: [MessageHandler(Filters.text, new_user)],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]

    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
