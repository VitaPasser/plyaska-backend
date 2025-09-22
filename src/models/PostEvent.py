import datetime
import logging
import pprint
from typing import List, Literal, Tuple, Optional, Annotated

import pymongo
from beanie import Indexed, Link
from pydantic import BaseModel, Field, create_model

from src.models.Promotion import Promotion
from src.models.User import User
from src.utils.models.BaseDocument import BaseDocument


class PromotionDeal(BaseModel):
    promotion_type: Link[Promotion]
    start_datetime: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end_datetime: datetime.datetime
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class Image(BaseModel):
    url: str
    description: str = None


class Location(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: Tuple[float, float]  # (longitude, latitude)


class PostEvent(BaseDocument):
    name: str
    description: Optional[str] = None
    author: Link[User]
    images: List[Image]
    location: Annotated[Location, Indexed(index_type=pymongo.GEOSPHERE)]
    promotions: List[PromotionDeal] = Field(default_factory=list)

#
# post_event_dump = PostEvent.model_json_schema(mode='serialization')
# logging.debug(pprint.pformat(post_event_dump))
# PostEventSchema = create_model(f"{PostEvent.__name__}Schema", **post_event_dump)

class PostEventNear(PostEvent):
    score: float
