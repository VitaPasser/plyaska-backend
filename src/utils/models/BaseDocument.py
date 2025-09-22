from typing import TypeVar, Type

from beanie import Document

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
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        auto_collection(cls)
