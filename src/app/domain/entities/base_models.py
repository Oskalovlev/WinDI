from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.app.domain.entities.short_annotate import ShortAnnotated
from src.app.database import Base


class BaseIntIDModel(Base):

    __abstract__ = True

    id: Mapped[ShortAnnotated.intpk]

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )
