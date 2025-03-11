from sqlalchemy.orm import Mapped, mapped_column

from src.app.services.database import Base
from src.app.domain.entities.base_models import BaseIntIDModel


class TokenModel(BaseIntIDModel, Base):
    access_token: Mapped[str] = mapped_column(nullable=False)
    token_type: Mapped[str]


class TokenPayloadModel(BaseIntIDModel, Base):
    sub: Mapped[str]


class NewPasswordModel(BaseIntIDModel, Base):
    token: Mapped[str] = mapped_column(nullable=False)
    new_password: Mapped[str] = mapped_column(nullable=False)
