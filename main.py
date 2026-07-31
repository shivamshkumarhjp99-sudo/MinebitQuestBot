import json
import time
import traceback

from checker import get_quests
from telegram_bot import send_message

print("🚀 Minebit Quest Bot Started...")

while True:

    try:
        current = get_quests()

        try:
            with open("storage.json", "r", encoding="utf-8") as f:
                old = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            old = []

        old_names = set()

        for item in old:
            if isinstance(item, dict):
                old_names.add(item.get("name"))
            elif isinstance(item, str):
                old_names.add(item)

        new_found = False

        for quest in current:

            if quest["name"] not in old_names:

                message = f"""🚨 NEW QUEST

📌 {quest['name']}

⭐ XP : {quest['xp']}

🔗 https://zealy.io/cw/minebit/questboard"""

                send_message(message)

                print(f"✅ Alert Sent -> {quest['name']}")

                new_found = True

        with open("storage.json", "w", encoding="utf-8") as f:
            json.dump(current, f, indent=4, ensure_ascii=False)

        if not new_found:
            print("✔ No New Quest")

    except Exception:
        print("❌ Error occurred:")
        traceback.print_exc()

    print("⏳ Checking again in 2 minutes...\n")
    time.sleep(120)