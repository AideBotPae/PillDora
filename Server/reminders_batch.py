import luigi
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from Server.database import DBMethods as methods


def create_reminders():
    data = methods.get_all_receipts()
    date = datetime.datetime.utcnow()
    for values in data:
        for i in range(values[2]):
            if i == 0:
                date_hour = date.replace(hour=7)
            elif i == 1:
                date_hour = date.replace(hour=15)
            elif i == 2:
                date_hour = date.replace(hour=23)

            methods.insert_reminders(user_id=values[0], cn=values[1], date=date_hour)


def delete_reminders():
    date = datetime.datetime.utcnow()
    methods.suprimir_reminders(date)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(func=create_reminders, trigger='cron', hour=1)
    scheduler.add_job(func=delete_reminders, trigger='cron', hour=2)
    scheduler.start()