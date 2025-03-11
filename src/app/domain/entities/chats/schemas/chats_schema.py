from src.app.domain.entities.base_schemas import PydanticBaseSchema


class ChatSchema(PydanticBaseSchema):

    title: str
    type_chat: str

    class Config:
        from_attributes = True
