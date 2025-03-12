from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.app.services.database import Base
from src.app.domain.entities.base_models import BaseIntIDModel


class UserModel(BaseIntIDModel, Base):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return (
            f"\nUser id: {self.id!r}"
            f"\nName: {self.name!r}"
            f"\nEmail: {self.email!r}"
        )
