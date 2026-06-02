from jose import JWTError, jwt

from app.core.config import settings


def decode_token(token: str) -> dict | None:
    """Проверяет JWT-токен пользователя."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )
        return payload
    except JWTError:
        return None
    