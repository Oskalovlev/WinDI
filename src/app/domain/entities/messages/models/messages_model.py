from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.database import Base
from src.app.domain.entities.base_models import BaseIntIDModel
if TYPE_CHECKING:
    from src.app.domain.entities import ChatModel  # noqa


class MessageModel(BaseIntIDModel, Base):

    _index = True

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(type_=TIMESTAMP(timezone=True))
    is_read: Mapped[bool] = mapped_column(default=False)

    chat = relationship("ChatModel", back_populates="messages")
    sender = relationship("UserModel", back_populates="messages_sent")
    group = relationship("GroupModel", back_populates="group_messages")

    def __repr__(self):
        return (
            f"\nMessage id: {self.id!r}"
            f"\nChat id: {self.chat_id!r}"
            f"\nSender id: {self.sender_id!r}"
            f"\nMessage text: {self.content[:20]!r}"
            f"\nIs read: {self.is_read!r}"
        )
