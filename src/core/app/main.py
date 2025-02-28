from fastapi import FastAPI

from src.core.app.config import app_settings
from src.core.routers.main_router import main_router as all_routers

app = FastAPI(
    title=app_settings.app.APP_TITLE,
    description=app_settings.app.DECCRIPION
)

app.include_router(all_routers)
