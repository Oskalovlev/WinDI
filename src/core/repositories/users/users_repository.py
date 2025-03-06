from typing import Optional, List

from fastapi.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

# from src.domain.entities import UsersModel as User
# from src.domain.entities.users import UserCreateSchema
from src.domain.entities.users.models.users_model import UserModel as User
from src.domain.entities.users.schemas.users_schema import UserCreateSchema


class UserRepository:

    @staticmethod
    async def create_user(
        user: UserCreateSchema,
        session: AsyncSession
    ) -> User:
        new_user = User(**user.model_dump())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def get_user_by_id(
        user_id: int,
        session: AsyncSession
    ) -> Optional[User]:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi_users(
        session: AsyncSession
    ) -> List[User]:
        users = await session.scalars(select(User)).all()
        return users

    @staticmethod
    async def update_user(
        user_id: int,
        session: AsyncSession,
        **kwargs
    ) -> Optional[User]:
        if not kwargs:
            raise ValueError("Поля для обновления не предусмотрены")
        query = (
            update(User).where(User.id == user_id)
            .values(kwargs).returning(User)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_user(
        self,
        user_id: int,
        session: AsyncSession
    ) -> bool:
        user = await self.get_user_by_id(user_id, session)
        if not user:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Пользователь с идентификатором {user_id}"
                       " не существует"
            )

        query = delete(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.rowcount > 0
