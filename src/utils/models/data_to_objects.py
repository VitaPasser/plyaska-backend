from typing import TypeVar

from pydantic import BaseModel

from src.utils.models.base_document import BaseDocument
from src.utils.models.base_model_future_document import DateArchive

ModelT = TypeVar("ModelT", bound=BaseDocument | DateArchive)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=type[BaseModel, DateArchive])
