import asyncio
import os
import random
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
from telegram import Bot


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
    "loyal 🛡️",
    "realistisch 🎯",
    "kreativ 🎨",
    "emotional intelligent 💗",
    "integer ♜",
    "selbstreflektiert 🧠️",
    "ausbalanciert ⚖️",
    "ehrlich 💬",
    "lebensfroh 😊",
    "rücksichtsvoll 🧑‍🤝‍🧑",
    "menschlich 🧍‍♂️",
    "respektvoll 🫡",
    "selbstständig 🐯",
    "engagiert 🧑‍🏭",
    "begeistert 🤩",
    "entspannt 😌",
    "aufrichtig 🧑‍⚖️",
    "flexibel 🎭",
    "unabhängig 🐺",
    "ausgeglichen 🧘‍♂️"
]

message_bag = MessageBag(MESSAGES)
bot = Bot(token=BOT_TOKEN)
LOCAL_TZ = ZoneInfo("Europe/Berlin")
last_sent_date = None


def log(msg):
    print(f"{datetime.utcnow()} - {msg}", flush=True)


async def send_message():
    global last_sent_date
    today = datetime.now(LOCAL_TZ).date()

    if last_sent_date == today:
        log("Message already sent today, skipping")
        return

    last_sent_date = today
    message = f"Du bist {message_bag.next()}"
    await bot.send_message(chat_id=CHAT_ID, text=message)


def seconds_until_next_run():
    now_utc = datetime.now(tz=ZoneInfo("UTC"))
    now_local = now_utc.astimezone(LOCAL_TZ)

    today_run_local = datetime.combine(
        now_local.date(),
        time(hour=9, minute=0),
        tzinfo=LOCAL_TZ
    )
    if now_local < today_run_local:
        next_run_local = today_run_local
    else:
        next_run_local = today_run_local + timedelta(days=1)

    next_run_utc = next_run_local.astimezone(ZoneInfo("UTC"))
    seconds = (next_run_utc - now_utc).total_seconds()
    return seconds, next_run_local


async def scheduler():
    log("Bot started")
    seconds, next_run = seconds_until_next_run()
    log(f"First message scheduled at {next_run}")
    await asyncio.sleep(seconds)

    while True:
        await send_message()
        seconds, next_run = seconds_until_next_run()
        log(f"Next message scheduled at {next_run}")
        await asyncio.sleep(seconds)


async def main():
    await scheduler()


if __name__ == "__main__":
    asyncio.run(main())
