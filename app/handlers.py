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


async def _is_admin(message: Message) -> bool:
    """У приватному чаті — завжди можна; у групі — лише адмін/власник."""
    if message.chat.type == "private":
        return True
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ("administrator", "creator")


@router.message(Command("poll"))
async def cmd_poll(message: Message):
    if not await _is_admin(message):
        await message.answer("Опитування можуть запускати лише адміни 🙃")
        return
    await send_game_poll(message.bot, message.chat.id)


@router.message(Command("chatid"))
async def cmd_chatid(message: Message):
    await message.answer(f"ID цього чату: {message.chat.id}")
