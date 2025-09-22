import datetime
from typing import List, Literal, Tuple, Optional, Annotated

import pymongo
from beanie import Indexed, Link, DecimalAnnotation
from pydantic import BaseModel, Field

from src.models.Promotion import Promotion
from src.models.User import User
from src.utils.models.BaseDocument import BaseDocument
from src.utils.models.BaseModelFutureDocument import BaseModelFutureDocument


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


class PostEventModel(BaseModelFutureDocument):
    name: str
    description: Optional[str] = None
    author: Link[User]
    images: List[Image]
    location: Annotated[Location, Indexed(index_type=pymongo.GEOSPHERE)]
    promotions: List[PromotionDeal] = Field(default_factory=list)


class PostEvent(PostEventModel, BaseDocument):
    pass


class PostEventNear(PostEventModel):
    score: DecimalAnnotation
    active_promotions: List[PromotionDeal]
