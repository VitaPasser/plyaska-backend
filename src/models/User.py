from pydantic import EmailStr

from src.utils.models.BaseDocument import BaseDocument
from src.utils.models.BaseModelBeforeDocument import BaseModelBeforeDocument


class UserModel(BaseModelBeforeDocument, BaseDocument):
    username: str
    email: EmailStr
    full_name: str = None
    disabled: bool = False

class User(UserModel, BaseDocument):
    pass