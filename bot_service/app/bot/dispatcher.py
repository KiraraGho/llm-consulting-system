from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from app.core.config import settings


# Увеличенный timeout для Telegram API.
session = AiohttpSession(timeout=120)

bot = Bot(
    token=settings.telegram_bot_token,
    session=session,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ),
)

dp = Dispatcher()
