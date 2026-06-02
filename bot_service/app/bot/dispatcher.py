from aiogram import Bot, Dispatcher

from app.core.config import settings


# Создаём объект Telegram-бота
bot = Bot(token=settings.telegram_bot_token)

# Dispatcher отвечает за маршрутизацию сообщений
dp = Dispatcher()
