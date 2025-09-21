from typing import Tuple

from beanie import WriteRules

from src.models.PostEvent import PostEvent, PromotionDeal, Image, Location
from src.models.User import User
from src.repositories.PostEventRepository import PostEventRepository
from src.utils.service.BaseService import BaseService
from src.services.PromotionService import PromotionService


class PostEventService(BaseService):

    def __init__(self,
                 logger, database,
                 promotion_service: PromotionService,
                 post_event_repository: PostEventRepository):
        self._promotionService = promotion_service
        self._postEventRepository = post_event_repository
        super().__init__(logger, database)

    async def find_near_post_events(self, coordinates: Tuple[float, float]):
        max_distance_in_meters = 8000000
        post_events = await (self._postEventRepository.
                             find_near_post_events(max_distance_in_meters, coordinates))
        return post_events

    async def get_by_id(self, post_event_id):
        return await PostEvent.find_one(PostEvent.id == post_event_id)
    
    async def add_promotion(self, post_event_id: str, promotion_id: str):
        post_event = await self.get_by_id(post_event_id)
        promotion = await self._promotionService.find_by_id(promotion_id)
        promotion_deal = await self._promotionService.create_deal(promotion)
        post_event.promotions.append(promotion_deal)
        return post_event.save(link_rule=WriteRules.DO_NOTHING)

    async def create_post_event(self, author: User,
                                promotion_deal: PromotionDeal | None = None):
        image1 = Image(url="http://example.com/image1.jpg",
                       description="An example image")
        image2 = Image(url="http://example.com/image2.jpg",
                       description="An example image two")
        location = Location(coordinates=(37.6173, 55.7558))
        promotions = []
        if promotion_deal:
            promotions = [promotion_deal]
        post_event = PostEvent(
            name="Sample Event",
            description="This is a sample event description.",
            author=author,
            images=[image1, image2],
            location=location,
            promotions=promotions
        )
        return await post_event.save(link_rule=WriteRules.DO_NOTHING)

    async def find_one_by_name(self):
        return await PostEvent.find_one(PostEvent.author.username == "user2",
                                        fetch_links=True)

    async def create(self, post_event: PostEvent):
        return await post_event.insert(link_rule=WriteRules.DO_NOTHING)