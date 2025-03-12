from datetime import datetime

from src.app.domain.entities.base_schemas import PydanticBaseSchema


class MessageReadSchema(PydanticBaseSchema):

    # chat_id: int
    sender_id: int
    recipient_id: int
    content: str
    # timestamp: datetime
    # is_read: bool


class MessageCreateSchema(PydanticBaseSchema):

    recipient_id: int
    content: str
