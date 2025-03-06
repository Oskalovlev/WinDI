from datetime import datetime

from sqlalchemy import ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.database import Base
from src.domain.entities.base_models import BaseIntIDModel


class MessageModel(BaseIntIDModel, Base):

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(String(5000), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(type_=TIMESTAMP(timezone=True))
    is_read: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return (
            f"\nMessage id: {self.id!r}"
            f"\nChat id: {self.chat_id!r}"
            f"\nSender id: {self.sender_id!r}"
            f"\nMessage text: {self.text[:20]!r}"
            f"\nIs read: {self.is_read!r}"
        )
