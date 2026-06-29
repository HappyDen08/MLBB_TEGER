"""Щоденна відправка опитування. Запускається за розкладом PythonAnywhere.

PythonAnywhere → вкладка Tasks → Scheduled task о 08:00 UTC (= 11:00 Київ влітку):
    python /home/<username>/ProjectForLudmila/send_poll.py

Скрипт шле опитування в CHAT_ID і одразу завершується (always-on не потрібен).
"""
import asyncio
import os

from dotenv import load_dotenv

from app.bot import make_bot
from app.poll import send_game_poll

load_dotenv()


async def main():
    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        raise RuntimeError("CHAT_ID не заданий (напр. -100123...). Дізнатись: команда /chatid у чаті.")

    bot = make_bot()
    try:
        await send_game_poll(bot, int(chat_id))
        print(f"Опитування надіслано в чат {chat_id}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
