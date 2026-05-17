import requests
from datetime import datetime
from config.settings import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID
)

LOG_FILE = "data/logs.txt"

def send_alert(vehicle, phone, message):

    print("\n====================")
    print(" SENDING TELEGRAM ALERT ")
    print("====================")

    print(f"Vehicle : {vehicle}")
    print(f"Phone   : {phone}")
    print(f"Message : {message}")

    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    print("\nTelegram Response:")
    print(response.json())

    save_log(vehicle, phone, message)

def save_log(vehicle, phone, message):

    with open(LOG_FILE, "a") as file:

        log_message = (
            f"{datetime.now()} | "
            f"{vehicle} | "
            f"{phone} | "
            f"{message}\n"
        )

        file.write(log_message)