# from datetime import datetime

from src.app.domain.entities.base_schemas import (
    PydanticBaseSchema, PydanticIntIDSchema
)


class MessageReadSchema(PydanticIntIDSchema):

    # chat_id: int
    sender_id: int
    recipient_id: int
    content: str
    # timestamp: datetime
    # is_read: bool


class MessageCreateSchema(PydanticBaseSchema):

    recipient_id: int
    content: str
