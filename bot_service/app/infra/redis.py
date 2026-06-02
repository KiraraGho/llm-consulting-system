from redis.asyncio import Redis

from app.core.config import settings


_redis_client: Redis | None = None


def get_redis() -> Redis:
    """
    Возвращает единый Redis-клиент
    Redis используется для хранения JWT
    привязанного к Telegram user_id
    """
    global _redis_client

    if _redis_client is None:
        _redis_client = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    return _redis_client
