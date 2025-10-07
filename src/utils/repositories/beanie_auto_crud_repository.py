from datetime import datetime
from typing import Type

from beanie import PydanticObjectId

from src.exceptions.errors.repository import NotFoundedError
from src.utils.models.data_to_objects import CreateSchemaT, ModelT, UpdateSchemaT
from src.utils.repositories.auto_crud_repository import AutoCRUDRepository


class BeanieAutoCRUDRepository(AutoCRUDRepository):
    def __init__(self, model: Type[ModelT]):
        super().__init__(model)

    async def create(self, item: CreateSchemaT | ModelT):
        obj: type[ModelT] = self.model(**item.model_dump())
        await obj.insert()
        return obj

    async def update_or_error(self, _id: PydanticObjectId, item: UpdateSchemaT | ModelT):
        obj = await self.model.get(_id)
        if not obj:
            raise NotFoundedError(detail=f"{self.model} by id={_id}")
        update_data = obj.model_copy(update=item.model_dump(exclude_unset=True))
        update_data.updated_at = datetime.now()
        await obj.set(update_data.model_dump(exclude_unset=True))
        return await obj.get(_id)

    async def update_or_create(self, _id: PydanticObjectId, item: UpdateSchemaT | ModelT):
        obj = await self.model.get(_id)
        if not obj:
            obj = self.create(item)
        update_data = obj.model_copy(update=item.model_dump(exclude_unset=True))
        update_data.updated_at = datetime.now()
        await obj.set(update_data.model_dump(exclude_unset=True))
        return await obj.get(_id)

    async def find_all(self):
        return await self.model.find_all().to_list()

    async def find_by_id(self, _id: PydanticObjectId):
        return await self.model.get(_id)

    async def find_by_id_or_error(self, _id: PydanticObjectId):
        obj = await self.find_by_id(_id)
        if not obj:
            raise NotFoundedError(detail=f"{self.model} by id={_id}")
        return obj

    async def delete(self, _id: PydanticObjectId):
        obj = await self.model.get(_id)
        if not obj:
            raise NotFoundedError(detail=f"{self.model} by id={_id}")
        await obj.delete()
