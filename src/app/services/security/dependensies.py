from datetime import datetime, timezone

from jwt import JWT
from jwt.exceptions import JWTDecodeError
from fastapi import Request, HTTPException, Depends, status

from src.app.services.config.security_config import get_auth_data
from src.app.services.dao.users.users_dao import UserDAO
from src.app.services.exeptions.statuses import (
    TokenExpiredException,
    TokenNoFoundException,
    NoJWTException,
    NoUserIDException
)


def get_token(request: Request):

    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenNoFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):

    try:
        auth_data = get_auth_data()
        payload = JWT.decode(
            token,
            auth_data=auth_data["secret_key"],
            algorithms=auth_data["algorithm"]
        )
    except JWTDecodeError:
        raise NoJWTException

    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise NoUserIDException

    user = await UserDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
