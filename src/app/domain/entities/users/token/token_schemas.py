from annotated_types import MinLen, MaxLen

from pydantic import Field

from src.app.entities.base_schemas import PydanticBaseSchema


class TokenSchema(PydanticBaseSchema):
    access_token: str
    token_type: str = "bearer"


class TokenPayloadSchema(PydanticBaseSchema):
    sub: str | None = None


class NewPasswordSchema(PydanticBaseSchema):
    token: str
    new_password: str = Field(MinLen(8), MaxLen(40))
