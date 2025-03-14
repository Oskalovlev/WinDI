from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.app.database import Base
from src.app.domain.entities.base_models import BaseIntIDModel


class ChatModel(BaseIntIDModel, Base):

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    type_chat: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return (
            f"\nChat id: {self.id!r}"
            f"\nTitle chat: {self.title[:20]!r}"
            f"\nType chat: {self.type_chat!r}"
        )
