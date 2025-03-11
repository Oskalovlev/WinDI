from fastapi import APIRouter, Response
# from fastapi.requests import Request
# from fastapi.responses import HTMLResponse

from src.app.services.exeptions.statuses import (
    UserAlreadyExistsException,
    IncorrectEmailOrPasswordException,
    PasswordMismatchException
)
from src.app.services.security.auth_users import (
    get_password_hash,
    authenticate_user,
    create_access_token
)
from src.app.services.dao.users.users_dao import UserDAO
from src.app.domain.entities.users.schemas.suser_schema import (
    SUserRegisterSchema,
    SUserAuthSchema
)

router = APIRouter()


@router.post("/register/")
async def register_user(user_data: SUserRegisterSchema) -> dict:

    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException("Пароли не совпадают")
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login/")
async def auth_user(
    response: Response,
    user_data: SUserAuthSchema
):

    check = await authenticate_user(
        email=user_data.email,
        password=user_data.password
    )
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(
        key="users_access_token", value=access_token, httponly=True
    )
    return {
        "ok": True,
        "access_token": access_token,
        "refresh_token": None,
        "message": "Авторизация успешна!"
    }


@router.post("/logout")
async def logout_user(response: Response):

    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}
