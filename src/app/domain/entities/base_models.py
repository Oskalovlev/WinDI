from sqlalchemy.orm import Mapped

from src.app.domain.entities.short_annotate import ShortAnnotated
from src.app.services.database import Base


class BaseIntIDModel(Base):

    __abstract__ = True

    id: Mapped[ShortAnnotated.intpk]
