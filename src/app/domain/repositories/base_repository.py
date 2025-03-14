from typing import Optional

# from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.entities.users.models.users_model import UserModel as User


class BaseRepository:

    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def create(
        self,
        obj_in,
        user: Optional[User] = None
    ):
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get(
        self,
        obj_id: int,
    ):
        db_obj = await self.session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalar_one_or_none()

    async def get_multi(self):
        db_objs = await self.session.scalars(select(self.model))
        return db_objs.all()

    async def update(
        self,
        db_obj,
        **kwargs
    ):
        # obj_data = jsonable_encoder(db_obj)
        # update_data = obj_in.model_dump(exclude_unset=True)

        # for field in obj_data:
        #     if field in update_data:
        #         setattr(db_obj, field, update_data[field])
        # self.session.add(db_obj)
        # await self.session.commit()
        # await self.session.refresh(db_obj)
        # return db_obj
        query = (
            update(self.model).where(self.model.id == db_obj)
            .values(kwargs).returning(self.model)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def remove(
        self,
        db_obj
    ) -> bool:
        # await self.session.delete(db_obj)
        # await self.session.commit()
        # return db_obj
        # obj = await self.get(db_obj, self.session)
        query = delete(self.model).where(self.model.id == db_obj)
        result = await self.session.execute(query)
        return result.rowcount > 0
