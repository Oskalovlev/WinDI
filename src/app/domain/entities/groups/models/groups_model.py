from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.database import Base
from src.app.domain.entities.base_models import BaseIntIDModel


class GroupModel(BaseIntIDModel, Base):

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    messages: Mapped[int] = mapped_column(
        ForeignKey("messages.id")
    )

    creator = relationship(
        "UserModel",
        back_populates="groups_created"
    )
    group_messages = relationship(
        "MessageModel",
        back_populates="group"
    )
    members = relationship(
         "UserModel",
         secondary="group_members",
         back_populates="groups"
    )

    def __repr__(self):
        return (
            f"\nGroup id: {self.id!r}"
            f"\nTitle group: {self.title!r}"
            f"\nCreator id: {self.creator_id!r}"
        )


class GroupMembersModel(BaseIntIDModel, Base):

    __tablename__ = "group_members"

    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
