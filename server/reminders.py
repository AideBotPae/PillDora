from server.database import Database
import datetime
import schedule
import time
import telegram


# THIS CLASS IS THE ONE THAT HAS THE TASK OF ACTUALIZING THE DAILY TABLE EVERY DAY WITH THE REMINDERS!
class Reminder:
    def __init__(self, arg):
        self.client = arg

    def daily_actualizations(self):
        # Every day at 01:00 the system will proceed to check if any reminder needs to be removed as expired
        schedule.every().day.at("01:00").do(self.checking_expirations)
        schedule.every().day.at("02:00").do(self.delete_history)
        schedule.every().hour.do(self.remind_information)
        time.sleep(10)
        self.test()
        while True:
            schedule.run_pending()
            # Sleeps for half an hour
            time.sleep(30)

    # Delete all reminders which has expired by end_date < today
    def test(self):
        bot = telegram.Bot('877926240:AAEuBzlNaqYM_kXbOMxs9lzhFsR7UpoqKWQ')
        print("Inside")
        self.client.show_current_aidebot_status(bot)

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
            now = now.strftime('%H:%M:%S')
            before_now = before_now.strftime('%H:%M:%S')
            # this will be extract afterwards
            query = '''SELECT national_code, time, user_id
                                       FROM aidebot.daily_reminders 
                                       WHERE time >= '{before_now}' and time>='{now}'
                                       '''.format(before_now=before_now, now=now)
            print(query)
            # till here

            data = db.query('''SELECT national_code, time, user_id
                                       FROM aidebot.daily_reminders 
                                       WHERE time >= '{before_now}' and time<='{now}'
                                       '''.format(before_now=before_now, now=now))
            self.client.send_reminders(data)

    # Delete information older than 3 days from history table
    def delete_history(self):
        with Database() as db:
            db.execute('''DELETE FROM aidebot.history WHERE (end_date<'{date}')'''.format(
                date=datetime.datetime.utcnow() - datetime.timedelta(days=3)))


if __name__ == "__main__":
    reminder = Reminder()
    reminder.daily_actualizations()
