from aiogram import F
from aiogram.types import Message

from app.bot.dispatcher import dp


@dp.message(F.text == "/start")
async def start_handler(message: Message) -> None:
    """Приветственное сообщение"""
    await message.answer(
    "Привет! 👋\n\n"
    "Я AI-консультант на базе LLM.\n"
    "Отправь мне сообщение, и я постараюсь помочь 🤖"
)


@dp.message(F.text == "/help")
async def help_handler(message: Message) -> None:
    """Команда помощи"""
    await message.answer(
        "Доступные команды:\n"
        "/start - запуск бота\n"
        "/help - помощь"
    )
