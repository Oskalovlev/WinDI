from pydantic_settings import BaseSettings, SettingsConfigDict

from src.app.services.config.settings_schemas import ExeptionsConfig


class ExeptionsSettings(BaseSettings):

    exeptions: ExeptionsConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore"
    )


exeption_details = ExeptionsSettings()
