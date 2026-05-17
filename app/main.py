# File: app/main.py

from app.checker import check_expiry

def start():
    print("\n==============================")
    print(" MV TAX ALERT BOT STARTED ")
    print("==============================\n")

    check_expiry()