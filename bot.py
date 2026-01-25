import os
import random
import asyncio
from datetime import datetime, timedelta, time
from telegram import Bot
import random

class MessageBag:
    def __init__(self, messages):
        self.messages = list(messages)
        self.bag = []

    def next(self):
        if not self.bag:
            self.bag = self.messages.copy()
            random.shuffle(self.bag)
        return self.bag.pop()

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

SEND_TIME_UTC = time(hour=9, minute=0)
message_bag = MessageBag(MESSAGES)

def log(msg):
    print(f"{datetime.utcnow()} - {msg}", flush=True)

bot = Bot(token=BOT_TOKEN)

async def send_message():
    message = f"Du bist {message_bag.next()}"
    await bot.send_message(chat_id=CHAT_ID, text=message)
    log(f"Message sent: {message}")

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