from fastapi import APIRouter

from src.app.interfaces.controllers import users_router
from src.app.interfaces.controllers import suser_router

main_router = APIRouter()

main_router.include_router(
    users_router, prefix="/users", tags=["User"]
)

main_router.include_router(
    suser_router, prefix="/auth", tags=["Auth"]
)
