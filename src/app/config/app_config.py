from pydantic_settings import BaseSettings, SettingsConfigDict

from src.app.config.settings_schemas import AppConfig


class AppSettings(BaseSettings):

    app: AppConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore"
    )


app_settings = AppSettings()
