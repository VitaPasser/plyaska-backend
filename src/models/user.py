from pydantic import EmailStr

from src.utils.models.base_document import BaseDocument
from src.utils.models.base_model_future_document import BaseModelFutureDocument


class UserModel(BaseModelFutureDocument):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool = False


class User(UserModel, BaseDocument):
    pass
