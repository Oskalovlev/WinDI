from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import EmailStr, SecretStr

from src.app.domain.entities.base_schemas import PydanticBaseSchema


class UserBaseSchema(PydanticBaseSchema):

    username: Annotated[str, MinLen(4), MaxLen(20)]
    email: EmailStr


class UserCreateSchema(UserBaseSchema):

    password: SecretStr


class UserUpdateSchema(UserBaseSchema):

    pass


class UserReadSchema(UserBaseSchema):

    class Config:
        from_attributes = True
