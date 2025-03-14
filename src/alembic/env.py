import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from src.app.config.alembic.base import Base
from src.app.config.database_config import db_settings as settings

config = context.config

# section = config.config_ini_section
# params_to_check = [
#     "POSTGRES_USER", "POSTGRES_PASS", "POSTGRES_HOST",
#     "POSTGRES_PORT", "POSTGRES_DB"
# ]

# for param_name in params_to_check:
#     default_value = getattr(settings.database, param_name)
#     config.get_section_option(section, param_name, default_value)

# config.set_main_option(
#     "sqlalchemy.url",
#     f"{settings.database.POSTGRES_ASYNC_PREFIX}"
#     F"{settings.database.POSTGRES_USER}:{settings.database.POSTGRES_PASS}"
#     F"@{settings.database.POSTGRES_HOST}/{settings.database.POSTGRES_DB}",
# )

# config.set_main_option(
#     "sqlalchemy.url", settings.database.DATABASE_URL_asyncpg
# )

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

print(settings.database.DATABASE_URL_asyncpg)
config.set_main_option(
    "sqlalchemy.url", settings.database.DATABASE_URL_asyncpg
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
