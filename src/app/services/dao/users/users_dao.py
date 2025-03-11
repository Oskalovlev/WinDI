from src.app.services.dao.base_dao import BaseDAO
from src.app.domain.entities.users.models.suser_model import SUserModel as User


class UserDAO(BaseDAO):

    model = User
