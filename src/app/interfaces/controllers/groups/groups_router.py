# import logging
import asyncio
from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Request,
    Depends
)

from src.app.database import get_async_session
from src.app.domain.repositories import group_repository
from src.app.domain.dao.groups.groups_dao import GroupDAO
from src.app.auth.dependensies import (
    get_current_user
)
from src.app.domain.entities import UserModel as User
from src.app.domain.entities import (
    GroupModel as Group,
    GroupCreateSchema,
    GroupUpdateSchema,
    GroupInDBSchema,
    GroupOutSchema
)

router = APIRouter()


@router.post(
    "/groups",
    response_model=GroupInDBSchema,
    # status_code=status.HTTP_201_CREATED
)
async def create_group(
    group: GroupCreateSchema,
    current_user: User = Depends(get_current_user)
):
    group_data = await GroupDAO.create(
        title=group.title,
        creator_id=current_user.id
    )
    return group_data


@router.put(
    "/groups/{group_id}/recipients",
    response_model=GroupInDBSchema
)
async def add_recipients_to_group(
    group_id: int,
    recipients: List[int],
    current_user: User = Depends(get_current_user)
):
    group_data = await GroupDAO.add_recipients(
        group_id=group_id,
        recipients=recipients
    )
    return group_data
