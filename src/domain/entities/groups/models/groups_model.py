from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.database import Base
from src.domain.entities.base_models import BaseIntIDModel


class GroupModel(BaseIntIDModel, Base):

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    chatters: Mapped[list[int]] = mapped_column(
        ForeignKey("users.id")
    )

    def __repr__(self):
        return (
            f"\nGroup id: {self.id!r}"
            f"\nCreator id: {self.creator_id!r}"
            f"\nTitle group: {self.title!r}"
            f"\nChatters: {self.chatters!r}"
        )
