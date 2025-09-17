import datetime
from typing import List, Literal, Tuple, Optional, Annotated

import pymongo
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field

from src.models.Promotion import Promotion


class PromotionDeal(BaseModel):
    promotion_type: Promotion
    start_datetime: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end_datetime: datetime.datetime
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    update_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str = None
    disabled: bool = False

class Image(BaseModel):
    url: str
    description: str = None

class Location(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: Tuple[float, float] = None  # (longitude, latitude)

class PostEvent(Document):
    name: str
    description: Optional[str] = None
    author: User
    images: List[Image]
    location: Annotated[Location, Indexed(index_type=pymongo.GEOSPHERE)]
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    promotions: List[PromotionDeal] = Field(default_factory=list)