from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    # HTTPException,
    # status
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.exeptions.statuses2 import ExceptionStatuses
from src.app.services.deps import (
    get_current_active_superuser,
    # CurrentUser,
    SessionDep
)
from src.app.domain.repositories.users.users_repository import UserRepository
from src.app.services.database import get_async_session
from src.app.domain.entities.users.models.users_model import UserModel as User
from src.app.domain.entities.users.schemas.users_schema import (
    UserReadSchema,
    UserCreateSchema,
    # UserUpdateSchema
)

router = APIRouter()


# @router.post(
#     "/",
#     response_model=UserCreateSchema,
#     response_model_exclude_none=True
# )
# async def create(
#     user: UserCreateSchema,
#     session: AsyncSession = Depends(get_async_session)
# ) -> User:

#     return await UserRepository.create_user(user=user, session=session)


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserCreateSchema
)
async def create_user(
    *, session: SessionDep, user: UserCreateSchema
) -> Optional[User]:
    user = await UserRepository.get_user_by_email(
        session=session, user_email=user.email
    )
    if user:
        raise ExceptionStatuses.status_400()

    user = await UserRepository.create_user(session=session, user=user)


@router.get(
    "/",
    response_model=UserReadSchema,
    response_model_exclude_none=True
)
async def get_multi(
    users: UserReadSchema,
    session: AsyncSession = Depends(get_async_session)
):
    return await UserRepository.get_multi_users(users=users, session=session)
