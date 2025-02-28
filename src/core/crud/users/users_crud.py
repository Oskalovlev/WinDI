from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

# from src.domain.entities import UsersModel as User
# from src.domain.entities.users import UserCreateSchema
from src.domain.entities.users.models.users_model import UsersModel as User
from src.domain.entities.users.schemas.users_schema import UserCreateSchema


class UsersCRUD:

    @staticmethod
    async def create_user(
        user: UserCreateSchema,
        session: AsyncSession
    ) -> User:
        new_user = user.model_dump()
        get_new_user = User(**new_user)
        session.add(get_new_user)
        await session.commit()
        await session.refresh(get_new_user)
        return get_new_user

    @staticmethod
    async def get_user_by_id(
        user_id: int,
        session: AsyncSession
    ) -> User:
        db_user = await session.execute(
            select(User).where(User.id == user_id)
        )
        return db_user.scalars().first()

    @staticmethod
    async def get_multi_users(
        session: AsyncSession
    ) -> list[User]:
        db_users = await session.execute(select(User))
        return db_users.scalars().all()

    @staticmethod
    async def update_user(
        user_id: int,
        session: AsyncSession,
        **kwargs
    ) -> User:
        update_user = update(User).where(User.id == user_id).values(kwargs)
        await session.execute(update_user)

    @staticmethod
    async def delete_user(
        user_id: int,
        session: AsyncSession
    ) -> None:
        delete_user = delete(User).where(User.id == user_id)
        await session.execute(delete_user)
