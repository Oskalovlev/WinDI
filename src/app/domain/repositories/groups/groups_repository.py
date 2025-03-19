from typing import Optional, List

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.repositories.base_repository import BaseRepository
from src.app.domain.entities import (
    UserModel as User,
    GroupModel as Group,
    GroupCreateSchema,
    GroupUpdateSchema,
    GroupInDBSchema,
    GroupOutSchema
)


class GroupRepository(BaseRepository):

    pass

    # def __init__(self, model, session: AsyncSession):
    #     self.model = model
    #     self.session = session

    # @classmethod
    # async def create(
    #     self,
    #     group: Group
    # ):
    #     self.session.add(group)
    #     await self.session.commit()
    #     await self.session.refresh(group)
    #     return group


group_repository = GroupRepository(model=Group, session=AsyncSession)
