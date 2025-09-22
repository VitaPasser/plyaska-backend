from typing import Annotated, Optional

from beanie import DecimalAnnotation
from pydantic import BaseModel, Field

from src.utils.models.BaseDocument import BaseDocument
from src.utils.models.BaseModelFutureDocument import BaseModelFutureDocument


class Money(BaseModel):
    amount: DecimalAnnotation
    currency: Annotated[str, Field(max_length=3, min_length=3)]  # USD, EUR, RUB


class PromotionModel(BaseModelFutureDocument):
    name: str
    description: Optional[str] = None
    power: Annotated[DecimalAnnotation, Field(ge=0)]
    duration: Annotated[int, Field(ge=0)]  # In seconds
    price: Money

class Promotion(PromotionModel, BaseDocument):
    pass