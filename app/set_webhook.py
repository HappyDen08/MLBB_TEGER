"""Одноразовий скрипт: реєструє вебхук у Telegram.

Запуск (з консолі PythonAnywhere або локально):
    WEBHOOK_URL=https://<username>.pythonanywhere.com/webhook python -m app.set_webhook
"""
import asyncio
import os

from app.bot import make_bot


async def main():
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError(
            "WEBHOOK_URL не заданий, напр. https://<username>.pythonanywhere.com/webhook"
        )

    bot = make_bot()
    try:
        await bot.set_webhook(
            url=webhook_url,
            secret_token=os.getenv("WEBHOOK_SECRET") or None,
            drop_pending_updates=True,
        )
        info = await bot.get_webhook_info()
        print(f"Webhook встановлено: {info.url}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
