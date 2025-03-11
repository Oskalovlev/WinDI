# from sqlalchemy import (
#     update as sqlalchemy_upadet,
#     delete as sqlachemy_delete,
#     func
# )
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from src.app.services.database import async_session_factory


class BaseDAO:

    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):

        async with async_session_factory() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):

        async with async_session_factory() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):

        async with async_session_factory() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):

        async with async_session_factory() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as err:
                    await session.rollback()
                    raise err
                return new_instance
