from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from datetime import datetime
from dotenv import load_dotenv
from storage_helper import load_quests

import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["📊 Status", "📋 Quests"],
        ["🔍 Check", "ℹ️ About"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
"""👋 Welcome to Minebit Quest Bot

🚀 Personal Zealy Quest Monitor

🟢 Status : Online
⏰ Auto Check : Every 5 Minutes
🔔 Instant Telegram Alerts

Choose an option below 👇""",
        reply_markup=reply_markup
    )


# ================= STATUS =================

async def status_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        quests = load_quests()

        text = f"""🟢 Minebit Quest Bot

🤖 Status : Online
☁ Platform : GitHub Actions
⏰ Check Interval : Every 5 Minutes

📋 Current Quests : {len(quests)}

🕒 Last Updated
{datetime.now().strftime("%d %b %Y | %I:%M:%S %p")}
"""

    except Exception as e:

        text = f"""🔴 Error

{e}
"""

    await update.message.reply_text(text)


# ================= QUESTS =================

async def quests_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        quests = load_quests()

        if not quests:
            await update.message.reply_text("❌ No quests found.")
            return

        text = f"📋 Minebit Current Quests ({len(quests)})\n\n"

        for i, quest in enumerate(quests, start=1):

            text += (
                f"{i}. {quest['name']}\n"
                f"⭐ XP : {quest['xp']}\n\n"
            )

        await update.message.reply_text(text)

    except Exception as e:

        await update.message.reply_text(f"❌ Error\n\n{e}")


# ================= CHECK =================

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = await update.message.reply_text("🔄 Reading latest quest database...")

    try:

        quests = load_quests()

        await msg.edit_text(
f"""✅ Database Loaded Successfully

📋 Current Quests : {len(quests)}

🕒 Checked At
{datetime.now().strftime("%d %b %Y | %I:%M:%S %p")}

⚡ Response Time : Instant
"""
        )

    except Exception as e:

        await msg.edit_text(f"❌ Error\n\n{e}")


# ================= HELP =================

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
"""📚 Minebit Quest Bot Commands

🚀 /start
Start the bot

📊 /status
View bot status

📋 /quests
View all current quests

🔍 /check
Read latest quest database

ℹ️ /about
About this bot

❓ /help
Show command list
"""
    )


# ================= ABOUT =================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
"""╔════════════════════════════╗
        🤖 Minebit Quest Bot
               v2.1
╚════════════════════════════╝

🚀 Smart Zealy Quest Monitor

👨‍💻 Developer
Shashank

🌐 Community
@OfficialSanviTech

━━━━━━━━━━━━━━━━━━━━

⚙️ Powered By

🐍 Python 3.11
🎭 Playwright
☁️ GitHub Actions
🤖 Telegram Bot API

━━━━━━━━━━━━━━━━━━━━

✨ Features

🟢 Auto Quest Detection
🔔 Instant Telegram Alerts
⚡ Fast Response
🛡️ Duplicate Protection
📊 Live Quest Database
⏰ Auto Check Every 5 Minutes

━━━━━━━━━━━━━━━━━━━━

💚 Thank you for using
Minebit Quest Bot!
"""
    )


async def about_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await about(update, context)


# ================= APP =================

app = Application.builder().token(BOT_TOKEN).build()

# Slash Commands

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("status", status_button))
app.add_handler(CommandHandler("quests", quests_button))
app.add_handler(CommandHandler("check", check_button))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("about", about))

# Keyboard Buttons

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^📊 Status$"),
        status_button
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^📋 Quests$"),
        quests_button
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🔍 Check$"),
        check_button
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^ℹ️ About$"),
        about_button
    )
)

print("🤖 Minebit Quest Bot v2.1 Started...")

app.run_polling()