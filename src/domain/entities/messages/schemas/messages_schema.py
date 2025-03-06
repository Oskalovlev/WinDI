from datetime import datetime

from src.domain.entities.base_schemas import PydanticBaseSchema


class MessageSchema(PydanticBaseSchema):

    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime
    is_read: bool

    class Config:
        from_attributes = True
