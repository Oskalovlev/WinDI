from datetime import timedelta, datetime, timezone
from typing import Optional, Any

import jwt
from passlib.context import CryptContext

from src.app.services.config.security_config import (
    security_settings as settings
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):  # noqa
#     to_encode = data.copy()
#     if expire_delta:
#         expire = datetime.now() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode,
#         settings.security.SECRET_KEY,
#         algorithm=settings.security.ALGORITHM
#     )
#     return encoded_jwt


def create_access_token(
    subject: str | Any,
    expire_delta: Optional[timedelta] = None
):
    if expire_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.security.SECRET_KEY,
        algorithm=settings.security.ALGORITHM
    )
    return encoded_jwt


def veryfy_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
