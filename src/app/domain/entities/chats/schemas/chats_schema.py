from src.app.domain.entities.base_schemas import (
    PydanticBaseSchema,
    PydanticIntIDSchema
)


class ChatBaseSchema(PydanticBaseSchema):

    title: str
    type_chat: str

    class Config:
        from_attributes = True


class ChatCreateSchema(ChatBaseSchema):
    pass


class ChatUpdateSchema(ChatBaseSchema):
    pass


class ChatInDBSchema(ChatBaseSchema, PydanticIntIDSchema):

    class Config:
        from_attributes = True


class ChatOutSchema(ChatBaseSchema, PydanticIntIDSchema):

    class Config:
        from_attributes = True
