from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.crud import users_crud
from src.core.database.database import get_async_session
from src.domain.entities.users.models.users_model import UsersModel as User
from src.domain.entities.users.schemas.users_schema import (
    UserReadSchema,
    UserCreateSchema,
    UserUpdateSchema
)

router = APIRouter()


@router.post(
    "/",
    response_model=UserCreateSchema,
    response_model_exclude_none=True
)
async def create(
    user: UserCreateSchema,
    session: AsyncSession = Depends(get_async_session)
) -> User:

    return await users_crud.create_user(user=user, session=session)


@router.get(
    "/",
    response_model=UserReadSchema,
    response_model_exclude_none=True
)
async def get_multi(
    users: UserReadSchema,
    session: AsyncSession = Depends(get_async_session)
):
    return await users_crud.get_multi_users(users=users, session=session)
