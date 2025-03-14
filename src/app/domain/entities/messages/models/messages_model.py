from datetime import datetime

from sqlalchemy import ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.app.database import Base
from src.app.domain.entities.base_models import BaseIntIDModel


class MessageModel(BaseIntIDModel, Base):

    _autoincrement = False
    _index = True

    # chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    # timestamp: Mapped[datetime] = mapped_column(type_=TIMESTAMP(timezone=True))
    # is_read: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return (
            f"\nMessage id: {self.id!r}"
            # f"\nChat id: {self.chat_id!r}"
            f"\nSender id: {self.sender_id!r}"
            f"\nRecipient id: {self.recipient_id!r}"
            f"\nMessage text: {self.content[:20]!r}"
            # f"\nIs read: {self.is_read!r}"
        )
