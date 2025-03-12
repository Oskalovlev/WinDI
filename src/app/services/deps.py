from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.config.security_config import security_settings
from src.app.services.exeptions.statuses2 import ExceptionStatuses
from src.app.services.database import get_async_session
from src.app.domain.entities.users.models.user_model import BUserModel as User
from src.app.domain.entities.users.token.token_models import (
    TokenPayloadModel as TokenPayload
)

reusable_OAuth2 = OAuth2PasswordBearer(
    tokenUrl="/token"  # tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
TokenDep = Annotated[str, Depends(reusable_OAuth2)]


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token,
            security_settings.security.SECRET_KEY,
            security_settings.security.ALGORITHM
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise ExceptionStatuses.status_401(detail="")

    user = session.get(User, token_data.sub)
    if not user:
        raise ExceptionStatuses.status_404()
    if not user.is_activ:
        raise ExceptionStatuses.status_400()
    return user


# async def get_current_user(
#     token: str = Depends(oauth2_schema),
#     session: AsyncSession
# ):
#     credentials_exception = ExceptionStatuses.status_401(
#         detail=NOT_VALIDATE_CREDINTIALS
#     )
#     try:
#         payload = jwt.decode(
#             token,
#             settings.security.SECRET_KEY,
#             algorithms=[settings.security.ALGORITHM]
#         )
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except jwt.JWTError:
#         raise credentials_exception from None

#     user = UserRepository.get_user_by_email(session=session, email=email)
#     if user is None:
#         raise credentials_exception
#     return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise ExceptionStatuses.status_403()
    return current_user
