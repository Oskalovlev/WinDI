from fastapi import APIRouter

from src.app.interfaces.controllers import (
    users_router, auth_router, chats_router
)

main_router = APIRouter()

main_router.include_router(
    users_router, prefix="/users", tags=["User"]
)

main_router.include_router(
    auth_router, prefix="/auth", tags=["Auth"]
)

main_router.include_router(
    chats_router, prefix="/chat", tags=["Chat"]
)
