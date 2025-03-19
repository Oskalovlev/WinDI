from typing import List

from sqlalchemy import select, and_, or_

from src.app.database import async_session_factory
from src.app.domain.dao.base_dao import BaseDAO
from src.app.domain.entities import (
    GroupModel as Group
)


class GroupDAO(BaseDAO):

    model = Group

    @classmethod
    async def create(cls, title: str, creator_id: int):

        async with async_session_factory() as session:
            query = select(cls.model).filter(
                title=title,
                creator_id=creator_id
            )
            # group = Group(title=title, creator_id=creator_id)
            session.add(query)
            session.commit()
            return query

    async def add_recipients(cls, group_id: int, recipients: List[int]):
        # Логика добавления участников в группу
        async with async_session_factory() as session:
            group = session.query(cls.model).filter(
                cls.model.id == group_id
            ).first()
            group.recipients.extend(recipients)
            session.commit()
            return group
