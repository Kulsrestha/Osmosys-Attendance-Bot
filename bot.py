import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, ALLOWED_TELEGRAM_USER_IDS
from oqsha_api import submit_attendance

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

def is_allowed(message: Message) -> bool:
    # Configure one or more Telegram numeric user IDs in .env.
    if not ALLOWED_TELEGRAM_USER_IDS:
        return False
    return bool(message.from_user and message.from_user.id in ALLOWED_TELEGRAM_USER_IDS)

@dp.message(Command("start"))
async def start(message: Message):
    if not is_allowed(message):
        await message.answer("Access is not configured for your Telegram account. Set ALLOWED_TELEGRAM_USER_IDS in .env.")
        return
    await message.answer("Oqsha attendance test bot ready.\nUse /checkin or /checkout.")

async def handle_attendance(message: Message, status: str):
    if not is_allowed(message):
        await message.answer("Not authorized. Configure your Telegram numeric user ID in ALLOWED_TELEGRAM_USER_IDS.")
        return
    await message.answer(f"Preparing {status} request...")
    try:
        result = await asyncio.to_thread(submit_attendance, status)
        await message.answer(result)
    except Exception as exc:
        logging.exception("Attendance test request failed")
        # Don't return credentials or request headers in chat.
        await message.answer(f"Request blocked or failed: {type(exc).__name__}: {exc}")

@dp.message(Command("checkin"))
async def checkin(message: Message):
    await handle_attendance(message, "CheckIn")

@dp.message(Command("checkout"))
async def checkout(message: Message):
    await handle_attendance(message, "CheckOut")

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing. Copy .env.example to .env and configure it.")
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
