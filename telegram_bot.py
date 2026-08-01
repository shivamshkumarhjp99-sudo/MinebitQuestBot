import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")


def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for chat_id in CHAT_IDS:

        chat_id = chat_id.strip()

        if not chat_id:
            continue

        payload = {
            "chat_id": chat_id,
            "text": message
        }

        response = requests.post(url, data=payload)

        print(f"Sent to {chat_id}")
        print("Status:", response.status_code)
        print("Response:", response.text)