import sqlite3
import requests

from datetime import datetime
import os

DB_FILE = "vehicles.db"

# -------------------------
# ULTRAMSG CONFIG
# -------------------------



INSTANCE_ID = os.environ.get("instance175927")

TOKEN = os.environ.get("yy0x5ac2xiym5wug")

# INSTANCE_ID = "instance175927"

# TOKEN = "yy0x5ac2xiym5wug"

# -------------------------
# SEND WHATSAPP FUNCTION
# -------------------------


def send_whatsapp_message(phone, message):

    url = f"https://api.ultramsg.com/" f"{INSTANCE_ID}" f"/messages/chat"

    payload = {"token": TOKEN, "to": f"91{phone}", "body": message}

    response = requests.post(url, data=payload)

    if response.status_code == 200:

        print("Message Sent")

    else:

        print("Error:")

        print(response.text)


# -------------------------
# DATABASE
# -------------------------

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()

cursor.execute(
    """

SELECT
    vehicle_number,
    expiry_date,
    phone,
    owner

FROM vehicles

"""
)

vehicles = cursor.fetchall()

today = datetime.today()

# -------------------------
# CHECK VEHICLES
# -------------------------

for vehicle in vehicles:

    vehicle_number = vehicle[0]

    expiry_date = vehicle[1]

    phone = vehicle[2]

    owner = vehicle[3]

    expiry = datetime.strptime(expiry_date, "%Y-%m-%d")

    days_left = (expiry - today).days

    # Send reminder if expiry
    # within 7 days

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

        send_whatsapp_message(phone, message)

        print("Message Sent")
