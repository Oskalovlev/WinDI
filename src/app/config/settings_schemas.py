from pydantic import BaseModel


class AppConfig(BaseModel):

    APP_TITLE: str = "WinDI"
    DESCRIPTION: str = "Мессенджер"

    class Config:
        env_file = ".env"


class DatabaseConfig(BaseModel):

    POSTGRES_ASYNC_PREFIX: str

    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

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
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


class ExeptionsConfig(BaseModel):

    USER_BY_ID_NOT_FOUND: str

    class Config:
        env_file = ".env"
