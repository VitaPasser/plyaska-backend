from typing import TypeVar

from pydantic import BaseModel

from src.utils.models.BaseDocument import BaseDocument
from src.utils.models.BaseModelFutureDocument import DateArchive

ModelT = TypeVar("ModelT", bound=BaseDocument | DateArchive)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=type[BaseModel, DateArchive])
