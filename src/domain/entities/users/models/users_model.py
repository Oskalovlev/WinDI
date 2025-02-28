from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.database import Base
from src.domain.entities.base_models import BaseIntIDModel


class UsersModel(BaseIntIDModel, Base):

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return (
            f"\nUser id: {self.id!r}"
            f"\nUsername: {self.username!r}"
            f"\nEmail: {self.email!r}"
        )
