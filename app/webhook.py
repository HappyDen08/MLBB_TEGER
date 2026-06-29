"""Webhook-режим для PythonAnywhere (Flask/WSGI).

На free-тарифі немає always-on процесів, тому long polling вбивається.
Натомість веб-додаток працює завжди — Telegram шле оновлення POST-ом на
/webhook, а ми передаємо їх у aiogram Dispatcher через фоновий event loop.

Це той самий підхід, що в ProjectRita.
"""
import asyncio
import logging
import os
import threading

from flask import Flask, abort, request

from aiogram import Dispatcher
from aiogram.types import Update

from app.bot import make_bot
from app.handlers import router

logging.basicConfig(level=logging.INFO)

bot = make_bot()
dp = Dispatcher()
dp.include_router(router)

# Секрет, яким Telegram підписує кожен запит (захист від чужих POST-ів)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

# Весь asyncio-код живе на одному фоновому лупі (WSGI-воркер синхронний).
# Луп створюємо ліниво, при першому запиті: uWSGI форкає воркера, а потоки
# форк не переживають — тож луп, запущений при імпорті, у воркері мертвий.
_loop = None
_loop_pid = None
_loop_lock = threading.Lock()


def get_loop():
    global _loop, _loop_pid
    with _loop_lock:
        if _loop is None or _loop_pid != os.getpid():
            _loop = asyncio.new_event_loop()
            _loop_pid = os.getpid()
            threading.Thread(target=_loop.run_forever, daemon=True).start()
            logging.info("Event loop started in pid %s", _loop_pid)
        return _loop


app = Flask(__name__)


@app.post("/webhook")
def telegram_webhook():
    if WEBHOOK_SECRET and request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        abort(403)
    loop = get_loop()
    update = Update.model_validate(request.get_json(force=True), context={"bot": bot})
    # Відповідаємо Telegram одразу, обробка йде у фоні
    future = asyncio.run_coroutine_threadsafe(dp.feed_update(bot, update), loop)
    future.add_done_callback(_log_update_errors)
    return "ok"


def _log_update_errors(future):
    exc = future.exception()
    if exc:
        logging.exception("Update processing failed", exc_info=exc)


@app.get("/")
def health():
    return "Bot is running (webhook mode) ✅"
