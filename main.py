import os
import requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from telegram import Bot

# Загружаем переменные окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "-1002665032382")
API_KEY = os.getenv("API_KEY", "164ad857d5184191934aedf61911f69b")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не установлен в .env или переменных окружения!")

bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dp = updater.dispatcher

# Пример команды

def start(update, context):
    update.message.reply_text("Бот запущен и работает!")

dp.add_handler(CommandHandler("start", start))

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен")
    updater.start_polling()
    updater.idle()
