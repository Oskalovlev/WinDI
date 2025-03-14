from sqlalchemy import select, and_, or_

from src.app.database import async_session_factory
from src.app.domain.dao.base_dao import BaseDAO
from src.app.domain.entities.messages.models.messages_model import (
    MessageModel as Message
)


class MessagesDAO(BaseDAO):

    model = Message

    @classmethod
    async def get_messages_between_users(cls, user_id_1: int, user_id_2: int):

        async with async_session_factory() as session:
            query = select(cls.model).filter(
                or_(
                    and_(
                        cls.model.sender_id == user_id_1,
                        cls.model.recipient_id == user_id_2
                    ),
                    and_(
                        cls.model.sender_id == user_id_2,
                        cls.model.recipient_id == user_id_1
                    )
                )
            ).order_by(cls.model.id)
            result = await session.execute(query)
            return result.scalars().all()
