from pydantic import BaseModel


class AppConfig(BaseModel):

    APP_TITLE: str = "WinDI"
    DESCRIPTION: str = "Мессенджер"


class DatabaseConfig(BaseModel):

    POSTGRES_ASYNC_PREFIX: str = "postgresql+asyncpg://"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASS: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    POSTGRES_DB: str = "windi"

    # DB_HOST: str
    # DB_PORT: str
    # DB_NAME: str
    # DB_USER: str
    # DB_PASS: str

    ECHO: bool

    @property
    def DATABASE_URL_asyncpg(self):
        return (
            f"{self.POSTGRES_ASYNC_PREFIX}"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASS}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


class SecurityConfig(BaseModel):

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


class ExeptionsConfig(BaseModel):

    USER_BY_ID_NOT_FOUND: str
