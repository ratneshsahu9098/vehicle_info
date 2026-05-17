import sqlite3
from datetime import datetime
from app.notifier import send_alert
from config.settings import ALERT_DAYS

DB_FILE = "vehicles.db"

def check_expiry():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT vehicle_number,
           expiry_date,
           phone
    FROM vehicles
    """)

    rows = cursor.fetchall()

    today = datetime.today()

    print("\nChecking vehicle expiry dates...\n")

    for row in rows:

        vehicle = row[0]
        expiry_date = row[1]
        phone = row[2]

        expiry = datetime.strptime(
            expiry_date,
            "%Y-%m-%d"
        )

        days_left = (expiry - today).days

        # Expired
        if days_left < 0:

            message = (
                f"WARNING: Vehicle {vehicle} "
                f"MV tax expired {-days_left} day(s) ago."
            )

            send_alert(vehicle, phone, message)

        # Expiring soon
        elif days_left <= ALERT_DAYS:

            message = (
                f"REMINDER: Vehicle {vehicle} "
                f"MV tax expires in {days_left} day(s)."
            )

            send_alert(vehicle, phone, message)

        else:
            print(f"{vehicle} is safe.")

    conn.close()