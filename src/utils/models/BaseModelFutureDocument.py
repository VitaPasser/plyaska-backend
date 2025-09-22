from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class BaseModelFutureDocument(BaseModel):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
