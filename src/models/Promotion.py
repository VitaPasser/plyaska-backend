import decimal
from typing import Annotated, Optional

from beanie import Document, DecimalAnnotation
from pydantic import BaseModel, Field


class Money(BaseModel):
    amount: DecimalAnnotation
    currency: Annotated[str, Field(max_length=3, min_length=3)]  # USD, EUR, RUB

class Promotion(Document):
    name: str
    description: Optional[str] = None
    power: Annotated[DecimalAnnotation, Field(ge=0)]
    duration: Annotated[int, Field(ge=0)] #In seconds
    price: Money