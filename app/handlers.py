"""Команди бота."""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.poll import send_game_poll

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привіт! Я щодня об 11:00 (Київ) кидаю опитування про гру.\n\n"
        f"ID цього чату: {message.chat.id}\n\n"
        "Команди:\n"
        "/poll — надіслати опитування зараз\n"
        "/chatid — показати ID чату"
    )


@router.message(Command("poll"))
async def cmd_poll(message: Message):
    await send_game_poll(message.bot, message.chat.id)


@router.message(Command("chatid"))
async def cmd_chatid(message: Message):
    await message.answer(f"ID цього чату: {message.chat.id}")
