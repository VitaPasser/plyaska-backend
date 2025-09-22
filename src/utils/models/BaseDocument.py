from datetime import datetime
from typing import Optional, TypeVar, Type

from beanie import Document, PydanticObjectId
from pydantic import Field

from src.utils.String import camel_to_db_name

T = TypeVar("T", bound=Type[Document])


def auto_collection(cls: T) -> T:
    if not hasattr(cls, "Settings"):
        class Settings:
            name: str

        cls.Settings = Settings

    cls.Settings.name = camel_to_db_name(cls.__name__)
    return cls


class BaseDocument(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        auto_collection(cls)
