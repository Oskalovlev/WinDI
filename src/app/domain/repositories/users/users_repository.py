from typing import Optional, List

import bcrypt
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.entities.users.models.users_model import UserModel as User
from src.app.domain.entities.users.schemas.users_schema import UserCreateSchema
from src.app.services.exeptions.statuses2 import ExceptionStatuses
from src.app.services.exeptions.details import USER_BY_ID_NOT_FOUND_404


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    async def create_user(self, user: UserCreateSchema) -> User:
        hashed_password = (
            bcrypt.hashpw(
                user.password.get_secret_value().encode("utf-8"),
                bcrypt.gensalt()
            )
        )
        new_user = User.verefy_password(
            plain_password=hashed_password
        )
        # new_user = User(**user.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    @staticmethod
    async def get_user_by_id(
        self,
        user_id: int
    ) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(
        user_email: str,
        session: AsyncSession
    ) -> Optional[User]:
        result = await session.execute(
            select(User).where(User.email == user_email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi_users(self) -> List[User]:
        users = await self.session.scalars(select(User))
        return users.all()

    @staticmethod
    async def update_user(
        self,
        user_id: int,
        **kwargs
    ) -> Optional[User]:
        if not kwargs:
            raise ValueError("Поля для обновления не предусмотрены")
        query = (
            update(User).where(User.id == user_id)
            .values(kwargs).returning(User)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_user(
        self,
        user_id: int
    ) -> bool:
        user = await self.get_user_by_id(user_id, self.session)
        if not user:
            # raise HTTPException(
            #     status_code=HTTP_404_NOT_FOUND,
            #     detail=f"Пользователь с идентификатором {user_id}"
            #            " не существует"
            # )
            raise ExceptionStatuses.status_404(
                detail=USER_BY_ID_NOT_FOUND_404.format(user_id)
            )

        query = delete(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.rowcount > 0
