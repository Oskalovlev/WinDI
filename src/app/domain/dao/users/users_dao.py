from src.app.domain.dao.base_dao import BaseDAO
from src.app.domain.entities.users.models.users_model import UserModel as User


class UserDAO(BaseDAO):

    model = User
