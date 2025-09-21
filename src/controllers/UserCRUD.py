from logging import Logger
from typing import List

from beanie import WriteRules
from fastapi import APIRouter

from src.models.User import User
from src.utils.controller.BaseController import BaseController
from src.utils.controller.RoutesUtils import get, post


class UserCRUD(BaseController):
    router = APIRouter(prefix='/user', tags=['User'])

    def __init__(self, logger: Logger):
        self._logger = logger
        super().__init__()

    @get("/", response_model=List[User])
    async def index(self):
        return User.find_all().to_list()

    @get("/{id}", response_model=User)
    async def find_by_id(self, id: str):
        return await User.find_one(User.id == id)

    @post("/", response_model=User)
    async def create(self, user: User):
        return await user.insert(link_rule=WriteRules.WRITE)