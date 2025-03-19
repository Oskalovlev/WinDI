from typing import List

from src.app.domain.entities.base_schemas import (
    PydanticBaseSchema, PydanticIntIDSchema
)


class GroupBaseSchema(PydanticBaseSchema):

    title: str
    recipient_ids: List[int] = []


class GroupCreateSchema(GroupBaseSchema):

    creator_id: int


class GroupUpdateSchema(GroupBaseSchema):

    pass


class GroupInDBSchema(GroupBaseSchema, PydanticIntIDSchema):

    creator_id: int

    class Config:
        from_attributes = True


class GroupOutSchema(GroupBaseSchema, PydanticIntIDSchema):

    creator_id: int

    class Config:
        from_attributes = True
