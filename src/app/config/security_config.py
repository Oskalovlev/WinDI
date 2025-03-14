from pydantic_settings import BaseSettings, SettingsConfigDict

from src.app.config.settings_schemas import SecurityConfig


class SecuritySettings(BaseSettings):

    security: SecurityConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore"
    )


security_settings = SecuritySettings()


def get_auth_data():
    return {
        "secret_key": security_settings.security.SECRET_KEY,
        "algorithm": security_settings.security.ALGORITHM
    }
