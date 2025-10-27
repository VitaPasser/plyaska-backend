import pickle
from datetime import datetime
from typing import Tuple

from beanie import PydanticObjectId, WriteRules
from fastapi import HTTPException
from redis.asyncio.client import Redis

from src import repositories, services
from src.exceptions.errors.repository import NotFoundedError
from src.models.post_event import SquareNearPostEvents, PostEventNear, PostEvent


async def find_near_post_events(
    coordinates: Tuple[float, float],
) -> list[PostEventNear]:
    max_distance_in_meters = 11000
    r: Redis = Redis(host="localhost", port=6379, db=0)
    near_post_events = await r.geosearch(
        PostEvent.get_settings().name,
        longitude=coordinates[0],
        latitude=coordinates[1],
        unit="m",
        width=250,
        height=250,
        sort="ASC",
        count=1,
    )
    if len(near_post_events) == 1:
        await r.close()
        return pickle.loads(near_post_events[0]).post_events

    post_events = await repositories.post_event.find_near_post_events(
        max_distance_in_meters, coordinates
    )
    square = SquareNearPostEvents(post_events=post_events)
    square_bytes = pickle.dumps(square)
    await r.geoadd(PostEvent.get_settings().name, coordinates + (square_bytes,))
    await r.close()

    return square.post_events


async def find_by_id(post_event_id: PydanticObjectId):
    try:
        return await repositories.post_event.find_by_id_or_error(post_event_id)
    except NotFoundedError:
        raise HTTPException(status_code=404, detail="Not found")


async def add_promotion(post_event_id: str, promotion_id: str):
    post_event = await find_by_id(PydanticObjectId(post_event_id))
    promotion = await services.promotion.find_by_id(PydanticObjectId(promotion_id))
    promotion_deal = await services.promotion.create_deal(promotion)
    post_event.promotions.append(promotion_deal)
    post_event.updated_at = datetime.now()
    return await post_event.save(link_rule=WriteRules.DO_NOTHING)
