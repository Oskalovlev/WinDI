from src.domain.entities.base_schemas import PydanticBaseSchema


class GroupSchema(PydanticBaseSchema):

    creator_id: int
    title: str
    chatters: list[int]

    class Config:
        from_attributes = True
