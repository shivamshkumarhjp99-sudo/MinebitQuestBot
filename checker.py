from playwright.sync_api import sync_playwright
import re

URL = "https://zealy.io/cw/minebit/questboard"

IGNORE = {
    "Home",
    "Search among my communities",
    "Create new community",
    "Discover communities",
    "Information",
    "Quests",
    "General",
    "Sprint",
    "Leaderboard",
    "Daily Challenge",
    "Today progress",
    "Complete Challenge",
    "Connect to Zealy",
    "Accept all",
    "Only necessary",
    "Customize",
    "Your privacy",
    "Minebit",
    "MineBit Community",
    "Invite Quests",
    "Start here",
    "Weekly",
    "Daily",
    "Xp"
}


def clean(text):
    return text.replace("\xa0", " ").strip()


def get_quests():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(viewport={"width": 1600, "height": 900})

        page.goto(URL, wait_until="networkidle")

        page.wait_for_timeout(5000)

        body = page.locator("body").inner_text()

        browser.close()

    lines = [clean(x) for x in body.split("\n") if clean(x)]

    quests = []

    i = 0

    while i < len(lines) - 2:

        name = clean(lines[i])

        if name in IGNORE:
            i += 1
            continue

        if lines[i + 1] != "Xp":
            i += 1
            continue

        try:
            xp = int(re.findall(r"\d+", lines[i + 2])[0])
        except:
            i += 1
            continue

        if len(name) < 5:
            i += 1
            continue

        if "cookie" in name.lower():
            i += 1
            continue

        if "privacy" in name.lower():
            i += 1
            continue

        quests.append({
            "name": name,
            "xp": xp
        })

        i += 3

    unique = []
    seen = set()

    for q in quests:
        if q["name"] not in seen:
            seen.add(q["name"])
            unique.append(q)

    return unique


if __name__ == "__main__":

    print("=" * 40)

    for quest in get_quests():

        print(f"{quest['name']} | XP {quest['xp']}")

    print("=" * 40)
    time.sleep(120)