from typing import TYPE_CHECKING

from beanie import PydanticObjectId

from src.models.user import User
from src.utils.models.data_to_objects import CreateSchemaT, UpdateSchemaT
from src.utils.repositories.beanie_auto_crud_repository import BeanieAutoCRUDRepository

__repository = BeanieAutoCRUDRepository(User)

__all__ = [f for f in __repository.export_methods().keys()]

if TYPE_CHECKING:

    async def create(item: CreateSchemaT | User) -> User: ...
    async def update_or_error(
        _id: PydanticObjectId, item: UpdateSchemaT | User
    ) -> User: ...
    async def update_or_create(
        _id: PydanticObjectId, item: UpdateSchemaT | User
    ) -> User: ...
    async def find_all() -> list[User]: ...
    async def find_by_id(_id: PydanticObjectId) -> User: ...
    async def find_by_id_or_error(_id: PydanticObjectId) -> User: ...
    async def delete(_id: PydanticObjectId) -> User: ...
