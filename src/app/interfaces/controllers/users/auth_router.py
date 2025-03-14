from typing import List

from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.app.exeptions.auth_exp import (
    UserAlreadyExistsException,
    IncorrectEmailOrPasswordException,
    PasswordMismatchException
)
from src.app.auth.auth_users import (
    get_password_hash,
    authenticate_user,
    create_access_token
)
from src.app.domain.dao.users.users_dao import UserDAO
from src.app.domain.entities.users.schemas.users_auth_schema import (
    UserRegisterSchema,
    UserAuthSchema,
    UserReadSchema
)

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/users", response_model=List[UserReadSchema])
async def get_users():
    users_all = await UserDAO.find_all()
    return [{"id": user.id, "name": user.name} for user in users_all]


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Страница авторизации"
)
async def get_categories(request: Request):

    return templates.TemplateResponse("auth.html", {"request": request})


@router.post("/register/")
async def register_user(user_data: UserRegisterSchema) -> dict:

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
    user_data: UserAuthSchema
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
