from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.settings_schemas import DatabaseConfig


class DatabaseSettings(BaseSettings):

    database: DatabaseConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore"
    )


db_settings = DatabaseSettings()
