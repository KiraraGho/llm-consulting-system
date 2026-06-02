import asyncio

from fastapi import FastAPI

from app.bot.dispatcher import bot, dp
from app.bot.handlers import *
from app.core.config import settings


def create_app() -> FastAPI:
    """Создаёт FastAPI-приложение Bot Service."""
    app = FastAPI(title=settings.app_name)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "service": settings.app_name,
            "env": settings.env,
        }

    return app


app = create_app()


async def run_bot() -> None:
    """Запуск Telegram-бота."""
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
    