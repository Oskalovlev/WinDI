from fastapi.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.repositories.users.users_repository import UserRepository


def authenticate_user(
        email: str,
        password: str,
        session: AsyncSession
):
    user = UserRepository.get_user_by_email(
        user_email=email, session=session
    )
    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Неверный пароль или почта"
        )
    return user
