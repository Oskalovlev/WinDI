from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr
)

from src.app.config.database_config import db_settings as settings

async_engine = create_async_engine(
    url=settings.database.DATABASE_URL_asyncpg,
    echo=settings.database.ECHO
)

async_session_factory = async_sessionmaker(async_engine, class_=AsyncSession)


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):

        name = cls.__name__.lower()
        if "model" in name:
            return name.replace("model", "s")


async def get_async_session():
    async with async_session_factory() as async_session:
        yield async_session
