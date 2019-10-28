from botui.bot import PillDora
from server.reminders import Reminder
import threading
from multiprocessing.dummy import Manager


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


if __name__ == "__main__":
    q = Manager().Queue()
    pilldora = PillDora()
    run_threaded(Reminder(pilldora).daily_actualizations)
    pilldora.main()
