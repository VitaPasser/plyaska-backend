from typing import Tuple

from beanie import WriteRules, PydanticObjectId
from fastapi import HTTPException

from src.models.PostEvent import PostEvent
from src.repositories import PostEventRepository
from src.services import PromotionService


async def find_near_post_events(coordinates: Tuple[float, float]):
    max_distance_in_meters = 8000000
    post_events = await PostEventRepository.find_near_post_events(max_distance_in_meters, coordinates)
    return post_events

async def find_by_id(post_event_id: PydanticObjectId):
    post_event = await PostEvent.get(post_event_id)
    if post_event is None:
        raise HTTPException(status_code=404, detail="Not found")
    return post_event

async def add_promotion(post_event_id: str, promotion_id: str):
    post_event = await find_by_id(PydanticObjectId(post_event_id))
    promotion = await PromotionService.find_by_id(PydanticObjectId(promotion_id))
    promotion_deal = await PromotionService.create_deal(promotion)
    post_event.promotions.append(promotion_deal)
    return await post_event.save(link_rule=WriteRules.DO_NOTHING)