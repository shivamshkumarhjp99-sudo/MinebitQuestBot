import json

STORAGE_FILE = "storage.json"


def load_quests():
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []