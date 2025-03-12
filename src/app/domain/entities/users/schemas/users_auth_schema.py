from pydantic import EmailStr, Field

from src.app.domain.entities.base_schemas import PydanticBaseSchema, PydanticIntIDSchema


class UserRegisterSchema(PydanticBaseSchema):

    email: EmailStr = Field(None, description="Электронная почта")
    password: str = Field(
        None, min_length=5, max_length=50,
        description="Пароль, от 5 до 50 символов"
    )
    password_check: str = Field(
        None, min_length=5, max_length=50,
        description="Пароль, от 5 до 50 символов"
    )
    name: str = Field(
        None, min_length=3, max_length=50,
        description="Имя, от 3 до 50 символов"
    )


class UserAuthSchema(PydanticBaseSchema):

    email: EmailStr = Field(None, description="Электронная почта")
    password: str = Field(
        None, min_length=5, max_length=50,
        description="Пароль, от 5 до 50 символов"
    )


class UserReadSchema(PydanticIntIDSchema):

    name: str = Field(
        None, min_length=3, max_length=50,
        description="Имя от 3 до 50 символов"
    )
