from pydantic import BaseModel


class AppConfig(BaseModel):

    APP_TITLE: str = "WinDI"
    DECCRIPION: str = "Мессенджер"


class DatabaseConfig(BaseModel):

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def DATABASE_URL_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
