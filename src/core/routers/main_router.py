from fastapi import APIRouter

from src.core.routers import users_router

main_router = APIRouter()

main_router.include_router(
    users_router, prefix="/users", tags=["User"]
)
