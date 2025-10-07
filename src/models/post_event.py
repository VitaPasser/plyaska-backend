import datetime
from typing import Annotated, List, Literal, Optional, Tuple

import pymongo
from beanie import DecimalAnnotation, Indexed, Link
from pydantic import BaseModel, Field

from src.models.promotion import Promotion
from src.models.user import User
from src.utils.models.base_document import BaseDocument
from src.utils.models.base_model_future_document import BaseModelFutureDocument


class PromotionDeal(BaseModel):
    promotion_type: Link[Promotion]
    start_datetime: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end_datetime: datetime.datetime
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class Image(BaseModel):
    url: str
    description: str


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
