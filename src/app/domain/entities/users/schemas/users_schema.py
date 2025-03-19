from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import EmailStr, SecretStr

from src.app.domain.entities.base_schemas import (
    PydanticBaseSchema,
    PydanticIntIDSchema
)


class UserBaseSchema(PydanticBaseSchema):

    name: Annotated[str, MinLen(4), MaxLen(20)]
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreateSchema(UserBaseSchema):

    password: SecretStr


class UserUpdateSchema(UserBaseSchema):

    pass


class UserInDBSchema(UserBaseSchema, PydanticIntIDSchema):

    password: SecretStr

    class Config:
        from_attributes = True


class UserOutSchema(UserBaseSchema, PydanticIntIDSchema):

    class Config:

        from_attributes = True
