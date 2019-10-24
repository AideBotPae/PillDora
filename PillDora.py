from botui.bot import PillDora
from server.reminders import Reminder
import threading

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

if __name__ == "__main__":
    run_threaded(Reminder().daily_actualizations)
    PillDora().main()
