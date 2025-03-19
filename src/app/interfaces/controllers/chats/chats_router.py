from fastapi import (
    APIRouter,
    Request,
    Depends
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.app.domain.dao.users.users_dao import UserDAO
from src.app.auth.dependensies import (
    get_current_user
)
from src.app.domain.entities.users.models.users_model import UserModel as User

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Chat Page"
)
async def get_chat_page(
    request: Request,
    user_data: User = Depends(get_current_user)
):
    users_all = await UserDAO.find_all()

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "user": user_data,
            "users_all": users_all
        }
    )
