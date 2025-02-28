from sqlalchemy.orm import Mapped

from src.domain.entities.short_annotate import ShortAnnotated
from src.core.database.database import Base


class BaseIntIDModel(Base):

    __abstract__ = True

    id: Mapped[ShortAnnotated.intpk]
