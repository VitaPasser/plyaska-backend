from typing import List

from fastapi import APIRouter

from src.models.Promotion import Promotion
from src.utils.controller.BaseController import BaseController
from src.services.PromotionService import PromotionService
from src.utils.controller.RoutesUtils import get, post


class PromotionCRUD(BaseController):
    router = APIRouter(prefix='/promotion', tags=['Promotion'])

    def __init__(self, promotion_service: PromotionService):
        self._promotionService = promotion_service
        super().__init__()

    @get('/', response_model=List[Promotion])
    async def index(self):
        return await self._promotionService.find_all()

    @post('/', response_model=Promotion)
    async def create(self) -> Promotion:
        return await self._promotionService.create()