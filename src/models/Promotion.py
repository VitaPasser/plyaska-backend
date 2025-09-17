import decimal
from typing import Annotated, Optional, Literal

from beanie import Document
from pydantic import BaseModel, Field


class Money(BaseModel):
    amount: decimal.Decimal
    currency: Annotated[str, Field(max_length=3, min_length=3)]  # USD, EUR, RUB

class Promotion(Document):
    name: str
    description: Optional[str] = None
    power: Annotated[decimal.Decimal, Field(ge=0)]
    price_per: Literal["second","minute","hour","day","week","month","year"] = "hour"
    duration: Annotated[decimal.Decimal, Field(ge=0)]
    price: Money