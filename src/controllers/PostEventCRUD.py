import logging
import pprint
from typing import List, Type

from src.models.PostEvent import PostEvent, PostEventNear
from src.services.PostEventService import find_near_post_events, add_promotion as add_promotion_service
from src.utils.controllers.AutoCRUD import CRUDRouter

logging.debug(f"Type PostEvent: {Type[PostEvent]}. PE: {PostEvent.__annotations__}.")
router = CRUDRouter(model=PostEvent, exclude=[CRUDRouter.find_all.__name__]).router


@router.get("/", response_model=List[PostEventNear])
async def index(longitude: float = 37.6173, latitude: float = 55.7558):
    near_post_events = await find_near_post_events((longitude, latitude))
    logging.debug(f"Found {pprint.pformat(near_post_events)} nearby post events")
    return near_post_events


@router.get("/{post_event_id}/add-promotion/{promotion_id}", response_model=PostEvent)
async def add_promotion(post_event_id: str, promotion_id: str):
    return await add_promotion_service(post_event_id, promotion_id)
