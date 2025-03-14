import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.app.database import Base
from src.app.domain.entities.base_models import BaseIntIDModel


class BUserModel(BaseIntIDModel, Base):

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return (
            f"\nUser id: {self.id!r}"
            f"\nUsername: {self.username!r}"
            f"\nEmail: {self.email!r}"
        )

    def verefy_password(self, plain_password: str) -> bool:
        return (bcrypt.checkpw(plain_password.encode("utf-8")),
                self.hashed_password.encode("utf-8"))
