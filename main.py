import json
import traceback

from checker import get_quests
from telegram_bot import send_message

print("🚀 Minebit Quest Bot Started...")

def main():
    current = get_quests()

    try:
        with open("storage.json", "r", encoding="utf-8") as f:
            old = json.load(f)
    except:
        old = []

    old_names = set()

    for item in old:
        if isinstance(item, dict):
            old_names.add(item["name"])
        elif isinstance(item, str):
            old_names.add(item)

    new_found = False

    for quest in current:

        if quest["name"] not in old_names:

            message = f"""🚨 NEW QUEST

📌 {quest['name']}

⭐ XP : {quest['xp']}

https://zealy.io/cw/minebit/questboard"""

            send_message(message)

            print("✅ Alert:", quest["name"])

            new_found = True

    with open("storage.json", "w", encoding="utf-8") as f:
        json.dump(current, f, indent=4, ensure_ascii=False)

    if not new_found:
        print("✔ No New Quest")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()

    print("✅ Finished")