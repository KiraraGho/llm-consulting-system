import asyncio

from aiogram import Bot

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import ask_openrouter


@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> None:
    """
    Celery-задача для LLM-запроса
    Worker получает задачу из RabbitMQ, вызывает OpenRouter 
    и отправляет ответ пользователю в Telegram
    """
    asyncio.run(_process_llm_request(tg_chat_id, prompt))


async def _process_llm_request(tg_chat_id: int, prompt: str) -> None:
    answer = await ask_openrouter(prompt)

    bot = Bot(token=settings.telegram_bot_token)
    await bot.send_message(tg_chat_id, answer)
    await bot.session.close()
