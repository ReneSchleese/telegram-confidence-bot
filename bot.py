import os
import random
import asyncio
from datetime import datetime
from telegram import Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

MESSAGES = [
    "loyal",
    "ein all-rounder",
    "realistisch",
    "kreativ",
    "emotional intelligent"
    "integer"
    "selbstreflektiert"
    "ausbalanciert"
    "ehrlich"
    "lebensfroh"
    "rücksichtsvoll"
    "menschlich"
    "respektvoll"
    "selbstständig"
    "engagiert"
    "begeistert"
    "entspannt"
    "aufrichtig"
    "flexibel"
    "vertrauenswürdig"
    "unabhängig"
    "ausgeglichen"
]

SEND_TIME_UTC = dtime(hour=9, minute=0)  # 09:00 UTC daily

def log(msg):
    print(f"{datetime.utcnow()} - {msg}", flush=True)

bot = Bot(token=BOT_TOKEN)

async def send_message():
    msg = random.choice(MESSAGES)
    await bot.send_message(chat_id=CHAT_ID, text=msg)
    log(f"Message sent: {msg}")

def seconds_until_next_run():
    now = datetime.utcnow()
    today_run = datetime.combine(now.date(), SEND_TIME_UTC)

    if now < today_run:
        next_run = today_run
    else:
        next_run = today_run + timedelta(days=1)

    return (next_run - now).total_seconds(), next_run

async def scheduler():
    log("Bot started")

    while True:
        seconds, next_run = seconds_until_next_run()
        log(f"Next message scheduled at {next_run} UTC")
        await asyncio.sleep(seconds)
        await send_message()

async def main():
    await scheduler()

if __name__ == "__main__":
    asyncio.run(main())