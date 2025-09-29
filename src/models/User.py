from pydantic import EmailStr

from src.utils.models.BaseDocument import BaseDocument
from src.utils.models.BaseModelFutureDocument import BaseModelFutureDocument


class UserModel(BaseModelFutureDocument):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool = False

class User(UserModel, BaseDocument):
    pass