from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.usecases.auth import AuthUseCase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Создаёт сессию БД на время одного HTTP-запроса."""
    async with AsyncSessionLocal() as session:
        yield session


def get_users_repo(session: AsyncSession = Depends(get_db)) -> UsersRepository:
    """Создаёт репозиторий пользователей."""
    return UsersRepository(session)


def get_auth_uc(
    users_repo: UsersRepository = Depends(get_users_repo),
) -> AuthUseCase:
    """Создаёт usecase авторизации."""
    return AuthUseCase(users_repo)


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Достаёт user_id из JWT."""
    payload = decode_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidTokenError()

    return int(user_id)
