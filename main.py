import csv
import time
import threading
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from telegram import Bot
import os
from telegram.ext import Updater, CommandHandler
from aiogram import types


updater = Updater("YOUR_TOKEN", use_context=True)
dp = updater.dispatcher

app = FastAPI()
templates = Jinja2Templates(directory="templates")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7739196769:AAFhSZeYk-v-sheZfc0ggl7E4T7S1xE1Ri0")
CHAT_ID = os.getenv("CHAT_ID", "-1002665032382")
API_KEY = os.getenv("API_KEY", "164ad857d5184191934aedf61911f69b")
BASE_URL = 'https://api.football-data.org/v4/matches'

running = True
log_file = "signals.csv"

def send_telegram_message(message):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"[Telegram Error] {e}")

def get_matches():
    headers = {"X-Auth-Token": API_KEY}
    params = {"status": "LIVE"}
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("matches", [])
    else:
        print(f"Ошибка запроса: {response.status_code}")
        return []

def analyze_matches():
    matches = get_matches()
    for match in matches:
        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        score = match['score']['halfTime']
        goals_home = score.get('homeTeam', 0)
        goals_away = score.get('awayTeam', 0)

        if goals_home > 0 or goals_away > 0:
            msg = f"ГОЛ в первом тайме! {home} vs {away} — {goals_home}:{goals_away}"
            send_telegram_message(msg)
            with open(log_file, "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([home, away, goals_home, goals_away, time.ctime()])

def background_loop():
    while running:
        print("Анализ матчей...")
        analyze_matches()
        time.sleep(600)

threading.Thread(target=background_loop, daemon=True).start()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    signals = []
    if os.path.exists(log_file):
        with open(log_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            signals = list(reader)[-10:]
    return templates.TemplateResponse("home.html", {"request": request, "signals": signals})

@app.get("/export")
async def export():
    return FileResponse(log_file, filename="signals.csv")

@app.post("/update")
async def update_settings(request: Request, chat_id: str = Form(...)):
    global CHAT_ID
    CHAT_ID = chat_id
    return RedirectResponse("/", status_code=302)
@dp.message_handler(commands=["test"])
async def test_message(message: types.Message):
    await message.answer("⚽️ Тест: Гол в первом тайме!")
