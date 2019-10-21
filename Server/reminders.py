import telegram
from Server.database import Database
import datetime
import schedule
import time

TOKEN_PROVE = '877926240:AAEuBzlNaqYM_kXbOMxs9lzhFsR7UpoqKWQ'
bot = telegram.Bot(TOKEN_PROVE)


# THIS CLASS IS THE ONE THAT HAS THE TASK OF ACTUALIZING THE DAILY TABLE EVERY DAY WITH THE REMINDERS!
class Reminder:
    def daily_actualizations(self):
        # Every day at 01:00 the system will proceed to check if any reminder needs to be removed as expired
        schedule.every().day.at("01:00").do(self.checking_expirations)
        schedule.every().hour.do(self.remind_information())

        while True:
            schedule.run_pending()
            # Sleeps for half an hour
            time.sleep(60 * 60 / 2)

    # Delete all reminders which has expired by end_date < today
      
    def checking_expirations(self):
        with Database() as db:
            today = str(datetime.date.today())
            db.execute('''DELETE FROM aidebot.daily_reminders WHERE (end_date<'{today}')'''.format(today=today))
            db.execute('''DELETE FROM aidebot.receipts WHERE (end_date<'{today}')'''.format(today=today))

      
    # Check for reminders of the last hour
    def remind_information(self):
        with Database() as db:
            now = datetime.datetime.now()
            before_now = now - datetime.timedelta(hours=1)
            now= now.strftime('%H:%M:%S')
            before_now=before_now.strftime('%H:%M:%S')
            # this will be extract afterwards
            query = '''SELECT national_code, time, user_id
                                       FROM aidebot.daily_reminders 
                                       WHERE time >= '{before_now}' and time>='{now}'
                                       '''.format(before_now=before_now, now=now)
            print(query)
            # till here

            data = db.query('''SELECT national_code, time, user_id
                                       FROM aidebot.daily_reminders 
                                       WHERE time >= '{before_now}' and time>='{now}'
                                       '''.format(before_now=before_now, now=now))
            for message in data:
                print(message)
                remind = "Remember to take " + str(message[0]) + " at " + message[1].strftime('%H:%M:%S')
                self.send_reminder(message[2], remind)

    # Sends a reminder using parsing
      
    def send_reminder(self, user_id, reminders):
        bot.send_message(chat_id=user_id,
                         text="*_`" + reminders + "`_*\n",
                         parse_mode=telegram.ParseMode.MARKDOWN)


if __name__ == "__main__":
    reminder = Reminder()
    reminder.daily_actualizations()
