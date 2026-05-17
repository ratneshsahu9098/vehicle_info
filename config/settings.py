# File: config/settings.py

from dotenv import load_dotenv
import os

load_dotenv()

ALERT_DAYS = 7

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")