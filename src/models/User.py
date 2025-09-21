from pydantic import EmailStr

from src.utils.models.BaseDocument import BaseDocument


class User(BaseDocument):
    username: str
    email: EmailStr
    full_name: str = None
    disabled: bool = False
