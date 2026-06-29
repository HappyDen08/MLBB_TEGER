"""Створення об'єкта Bot з проксі (потрібно для free PythonAnywhere)."""
import logging
import os
from pathlib import Path

from aiogram import Bot
from dotenv import load_dotenv

# Явний шлях до .env у корені проєкту — щоб працювало і у веб-додатку (WSGI),
# і в Scheduled task, де робоча тека може бути іншою.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def make_bot() -> Bot:
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token or bot_token == "your_bot_token_here":
        raise RuntimeError("BOT_TOKEN не заданий!")

    # На безкоштовному тарифі PythonAnywhere вихід в інтернет лише через проксі.
    session = None
    proxy_url = os.getenv("http_proxy") or os.getenv("HTTP_PROXY")
    if proxy_url:
        from aiogram.client.session.aiohttp import AiohttpSession
        session = AiohttpSession(proxy=proxy_url)
        logging.info("Using proxy: %s", proxy_url)

    return Bot(token=bot_token, session=session)
