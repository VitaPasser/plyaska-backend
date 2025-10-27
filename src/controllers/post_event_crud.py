from typing import List

from src.models.post_event import PostEvent, PostEventCreate, PostEventNear
from src.services.post_event import (
    add_promotion as add_promotion_service,
)
from src.services.post_event import (
    find_near_post_events,
)
from src.utils.controllers.crud_router import CRUDRouter

router = CRUDRouter(
    model=PostEvent,
    create_schema=PostEventCreate,
    exclude=[CRUDRouter.find_all.__name__],
    find_all_cached=False,
).router


@router.get("/", response_model=List[PostEventNear])
async def index(longitude: float, latitude: float):
    near_post_events = await find_near_post_events((longitude, latitude))
    return near_post_events


@router.get("/{post_event_id}/add-promotion/{promotion_id}", response_model=PostEvent)
async def add_promotion(post_event_id: str, promotion_id: str):
    return await add_promotion_service(post_event_id, promotion_id)
