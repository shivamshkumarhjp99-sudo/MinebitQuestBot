import requests
from config import BOT_TOKEN, CHAT_ID

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    response = requests.post(url, json=data)

    print("Status:", response.status_code)
    print("Response:", response.text)