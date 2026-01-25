import os
import random
import asyncio
from datetime import datetime
from telegram import Bot

# --- Configuration ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Set TEST_MODE=True to send messages every minute for testing
TEST_MODE = True  # <-- switch to False for production daily schedule

# Messages to choose from
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

# Helper function to log with timestamp and flush
def log(msg: str):
    print(f"{datetime.utcnow()} - {msg}", flush=True)

# Create bot instance
bot = Bot(token=BOT_TOKEN)

# Async function to send a Telegram message
async def send_message():
    message = f"Du bist {random.choice(MESSAGES)}"
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        log(f"Message sent: {message}")
    except Exception as e:
        log(f"Error sending message: {e}")

# Async function for periodic health ping
async def health_ping():
    log("Bot alive, waiting for next scheduled message...")

# Scheduler loop
async def scheduler_loop():
    while True:
        now = datetime.utcnow()
        if TEST_MODE:
            # Send every minute
            await send_message()
            await health_ping()
            await asyncio.sleep(60)  # wait 1 minute
        else:
            # Production: send daily at 09:00 UTC
            if now.hour == 9 and now.minute == 0:
                await send_message()
            await health_ping()
            await asyncio.sleep(30)  # check every 30 seconds

# --- Entry point ---
async def main():
    log("Bot started!")
    await scheduler_loop()

# Run the async main loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Bot stopped manually.")
