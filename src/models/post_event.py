import datetime
from typing import Annotated, List, Literal, Optional, Tuple

import pymongo
from beanie import (
    DecimalAnnotation,
    Indexed,
    Link,
)
from pydantic import Field

from src.models.promotion import Promotion
from src.models.user import User
from src.utils.models.base_document import BaseDocument
from src.utils.models.base_model import BaseModel
from src.utils.models.base_model_future_document import (
    BaseModelFutureDocument,
    DateArchive,
)


class PromotionDealCore(BaseModel):
    promotion_type: Link[Promotion]
    start_datetime: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end_datetime: datetime.datetime


class PromotionDeal(PromotionDealCore, DateArchive): ...


class PromotionDealCreate(PromotionDealCore):
    promotion_type: str  # Promotion ID


class Image(BaseModel):
    url: str
    description: str


class Location(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: Tuple[float, float]  # (longitude, latitude)


class PostEventCore(BaseModel):
    name: str
    description: Optional[str] = None
    author: Link[User]
    images: List[Image]
    location: Annotated[Location, Indexed(index_type=pymongo.GEOSPHERE)]
    promotions: List[PromotionDeal] = Field(default_factory=list)


class PostEventCreate(PostEventCore):
    author: str  # User ID
    promotions: List[PromotionDealCreate] | None = Field(default_factory=list)


class PostEventModel(BaseModelFutureDocument, PostEventCore): ...


class PostEventNear(PostEventModel):
    score: DecimalAnnotation
    active_promotions: List[PromotionDeal]


class SquareNearPostEvents(BaseModel):
    post_events: list[PostEventNear]


class PostEvent(PostEventModel, BaseDocument): ...
