from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.database import Base
from src.app.domain.entities.base_models import BaseIntIDModel
from src.app.domain.entities.groups.models.groups_model import GroupModel


class UserModel(BaseIntIDModel, Base):

    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    messages_sent = relationship(
        "MessageModel",
        back_populates="sender"
    )
    groups_created = relationship(
        "GroupModel",
        foreign_keys=[GroupModel.creator_id],
        back_populates="creator"
    )
    groups = relationship(
        "GroupModel",
        secondary="group_members",
        back_populates="members"
    )

    def __repr__(self):
        return (
            f"\nUser id: {self.id!r}"
            f"\nName: {self.name!r}"
            f"\nEmail: {self.email!r}"
        )
