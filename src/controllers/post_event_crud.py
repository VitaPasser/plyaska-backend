from typing import List

from src.models.post_event import PostEvent, PostEventNear
from src.services.post_event import (
    add_promotion as add_promotion_service,
)
from src.services.post_event import (
    find_near_post_events,
)
from src.utils.controllers.crud_router import CRUDRouter

router = CRUDRouter(model=PostEvent, exclude=[CRUDRouter.find_all.__name__]).router


@router.get("/", response_model=List[PostEventNear])
async def index(longitude: float = 37.6173, latitude: float = 55.7558):
    near_post_events = await find_near_post_events((longitude, latitude))
    return near_post_events


@router.get("/{post_event_id}/add-promotion/{promotion_id}", response_model=PostEvent)
async def add_promotion(post_event_id: str, promotion_id: str):
    return await add_promotion_service(post_event_id, promotion_id)
