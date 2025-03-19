from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.database import Base
from src.app.domain.entities.base_models import BaseIntIDModel


class ChatModel(BaseIntIDModel, Base):

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    type_chat: Mapped[str] = mapped_column(nullable=False)
    is_group_chat: Mapped[bool] = mapped_column(Boolean, default=False)

    messages = relationship("MessageModel", back_populates="chat")

    def __repr__(self):
        return (
            f"\nChat id: {self.id!r}"
            f"\nTitle chat: {self.title[:20]!r}"
            f"\nType chat: {self.type_chat!r}"
            f"\nIs group chat: {self.is_group_chat!r}"
        )
