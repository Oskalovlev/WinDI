from datetime import timedelta, datetime, timezone

import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from src.app.services.config.security_config import get_auth_data
from src.app.services.dao.users.users_dao import UserDAO


def create_access_token(data: dict) -> str:

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=366)
    to_encode.update({"exp": expire})

    auth_data = get_auth_data()
    encode_jwt = jwt.encode(
        to_encode,
        key=auth_data["secret_key"],
        algorithm=auth_data["algorithm"]
    )
    return encode_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def veryfy_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user or veryfy_password(
        plain_password=password,
        hashed_password=user.hashed_password
    ) is False:
        return None
    return user
