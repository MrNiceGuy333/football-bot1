from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
import os
from match_analyzer import analyze_matches
from logger import log_signal

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Бот активен и следит за матчами ⚽")

def check_matches(update: Update, context: CallbackContext):
    signals = analyze_matches()
    if signals:
        for s in signals:
            update.message.reply_text(s)
    else:
        update.message.reply_text("Пока ничего интересного.")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("check", check_matches))
