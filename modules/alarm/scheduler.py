import schedule
import time

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)