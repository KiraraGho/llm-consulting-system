from aiogram import F
from aiogram.types import Message

from app.bot.dispatcher import dp
from app.core.jwt import decode_token
from app.infra.redis import get_redis


@dp.message(F.text == "/start")
async def start_handler(message: Message) -> None:
    await message.answer(
        "Привет! 👋\n\n"
        "Я AI-консультант на базе большой языковой модели\n"
        "Для авторизации отправь:\n"
        "/token ВАШ_JWT_ТОКЕН"
    )


@dp.message(F.text == "/help")
async def help_handler(message: Message) -> None:
    await message.answer(
        "Доступные команды:\n\n"
        "/start - запуск бота\n"
        "/help - помощь\n"
        "/token <jwt> - авторизация"
    )


@dp.message(F.text.startswith("/token "))
async def token_handler(message: Message) -> None:
    """Проверяет JWT и сохраняет его в Redis"""
    token = message.text.replace("/token ", "").strip()
    payload = decode_token(token)

    if payload is None:
        await message.answer("Неверный или истёкший JWT-токен")
        return

    redis = get_redis()
    tg_user_id = message.from_user.id

    await redis.set(
        f"token:{tg_user_id}",
        token,
        ex=60 * 60,
    )

    await message.answer(
        "Авторизация успешна!\n\n"
        f"User ID: {payload.get('sub')}\n"
        f"Role: {payload.get('role')}"
    )


@dp.message(F.text)
async def text_handler(message: Message) -> None:
    """
    Обрабатывает обычный текст
    Пока только проверяем, есть ли сохранённый JWT
    """
    redis = get_redis()
    tg_user_id = message.from_user.id

    token = await redis.get(f"token:{tg_user_id}")
    if token is None:
        await message.answer(
            "Вы не авторизованы.\n\n"
            "Сначала получите JWT в Auth Service и отправьте:\n"
            "/token ВАШ_JWT_ТОКЕН"
        )
        return

    payload = decode_token(token)
    if payload is None:
        await redis.delete(f"token:{tg_user_id}")
        await message.answer(
            "Ваш токен истёк или недействителен.\n"
            "Авторизуйтесь заново через /token."
        )
        return

    await message.answer(
        "Вы авторизованы.\n"
        "Следующим шагом я буду отправлять ваш запрос в LLM."
    )
