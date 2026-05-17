# File: app/scheduler.py
import schedule
import time
from app.checker import check_expiry

def start_scheduler():

    print("\nMV TAX BOT SCHEDULER STARTED...\n")

    # Run every day at 9:00 AM
    schedule.every().day.at("09:00").do(check_expiry)

    # Run once immediately
    check_expiry()

    while True:

        schedule.run_pending()
        time.sleep(1)