from src.app.domain.entities.base_schemas import (
    PydanticBaseSchema, PydanticIntIDSchema
)


class MessageBaseSchema(PydanticBaseSchema):
    content: str


class MessageCreateSchema(MessageBaseSchema):
    chat_id: int
    sender_id: int


class MessageUpdateSchema(MessageBaseSchema):
    pass


class MessageInDBSchema(MessageBaseSchema, PydanticIntIDSchema):
    chat_id: int
    sender_id: int
    recipient_id: int

    class Config:
        from_attributes = True


class MessageOutSchema(MessageBaseSchema, PydanticIntIDSchema):

    chat_id: int
    sender_id: int

    class Config:
        from_attributes = True
