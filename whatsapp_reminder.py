import sqlite3
import pywhatkit
import pyautogui
import time

from datetime import datetime

DB_FILE = "vehicles.db"

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()

cursor.execute("""

SELECT
    vehicle_number,
    expiry_date,
    phone,
    owner

FROM vehicles

""")

vehicles = cursor.fetchall()

today = datetime.today()

for vehicle in vehicles:

    vehicle_number = vehicle[0]

    expiry_date = vehicle[1]

    phone = vehicle[2]

    owner = vehicle[3]

    expiry = datetime.strptime(
        expiry_date,
        "%Y-%m-%d"
    )

    days_left = (
        expiry - today
    ).days

    # Send only if expiry within 7 days

    if days_left <= 7:

        message = f"""

🚗 MV Tax Reminder

Hello {owner},

Vehicle:
{vehicle_number}

Tax expiry date:
{expiry_date}

Please renew soon.

"""

        print(message)

        time.sleep(5)

        pywhatkit.sendwhatmsg_instantly(

            f"+91{phone}",

            message,

            wait_time=30,

            tab_close=False
        )

        time.sleep(5)

        pyautogui.press("enter")

        print("Message Sent")