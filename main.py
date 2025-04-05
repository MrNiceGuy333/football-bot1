import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from telegram import Update
from bot import dispatcher, bot
from logger import get_logs

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    logs = get_logs()
    return templates.TemplateResponse("index.html", {"request": request, "logs": logs})

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    from telegram import Bot
    webhook_url = os.getenv("WEBHOOK_URL")
    await Bot(os.getenv("BOT_TOKEN")).setWebhook(webhook_url + "/webhook")
