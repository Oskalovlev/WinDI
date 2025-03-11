from src.app.domain.entities.base_schemas import PydanticBaseSchema


class GroupSchema(PydanticBaseSchema):

    creator_id: int
    title: str
    recipients_id: list[int]

    class Config:
        from_attributes = True
