import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from Server.database import DBMethods as methods


def delete_reminders():
    date = datetime.datetime.utcnow()
    methods.suprimir_reminders(date)
