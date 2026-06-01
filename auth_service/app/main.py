from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.api.router import router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Создаёт таблицы БД при старте приложения"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


def create_app() -> FastAPI:
    """Собирает FastAPI-приложение Auth Service"""
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )

    app.include_router(router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "service": settings.app_name,
            "env": settings.env,
        }

    return app


app = create_app()
