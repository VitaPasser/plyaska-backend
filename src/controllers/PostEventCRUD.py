from logging import Logger
from typing import List

from fastapi import APIRouter

from src.models.PostEvent import PostEvent
from src.utils.controller.BaseController import BaseController
from src.services.PostEventService import PostEventService
from src.services.PromotionService import PromotionService
from src.utils.controller.RoutesUtils import get, post


class PostEventCRUD(BaseController):
    router = APIRouter(prefix='/post-event', tags=['Post Event'])

    def __init__(self, logger: Logger,
                 post_event_service: PostEventService,
                 promotion_service: PromotionService):
        self._logger = logger
        self._postEventService = post_event_service
        self._promotionService = promotion_service
        super().__init__()

    @get("/", response_model=List[PostEvent])
    async def index(self, longitude: float = 37.6173, latitude: float = 55.7558):
        return await self._postEventService.find_near_post_events((longitude, latitude))

    @get("/{id}", response_model=PostEvent)
    async def find_by_id(self, id: str):
        return await self._postEventService.get_by_id(id)

    @get("/{post_event_id}/add-promotion/{promotion_id}", response_model=PostEvent)
    async def add_promotion(self, post_event_id: str, promotion_id: str):
        return await self._postEventService.add_promotion(post_event_id, promotion_id)

    @post("/", response_model=PostEvent)
    async def create(self, post_event: PostEvent):
        return await self._postEventService.create(post_event)