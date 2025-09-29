import logging
from datetime import datetime
from enum import Enum
from http import HTTPMethod
from typing import Generic, Type, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from fastapi.routing import APIRoute
from pydantic import BaseModel

from src.utils.models.BaseDocument import BaseDocument
from src.utils.models.CreateUpdateDTOMaker import make_create_schema, make_update_schema

ModelT = TypeVar("ModelT", bound=BaseDocument)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class CRUDRouter(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    """
    Example::

        from pydantic import BaseModel

        class UserModel(BaseModel):
            name: str

        class UserCreate(BaseModel):
            name: str

        router = CRUDRouter[UserModel, UserCreate, UserCreate](
            model=UserModel,
            create_schema=UserCreate,
            update_schema=UserCreate
            ).router
    """

    def __init__(
            self,
            model: Type[ModelT],
            create_schema: Type[CreateSchemaT] | None = None,
            update_schema: Type[UpdateSchemaT] | None = None,
            prefix: str | None = None,
            tags: list[str | Enum] | None = None,
            exclude: list[str] | None = None,
    ):
        if exclude is None:
            exclude = []
        self.model = model
        self.create_schema = create_schema or make_create_schema(model)
        self.update_schema = update_schema or make_update_schema(model)
        self.prefix = prefix or f"/{model.__name__.lower()}s"
        self.router = APIRouter(prefix=self.prefix, tags=tags or [model.__name__])

        # change type "item" parameter
        self.create = self._create(self.create_schema)
        self.update = self._update(self.update_schema)

        routes_define = {
            self.create.__name__: lambda: self.router.post("/", response_model=model)(self.create),
            self.find_all.__name__: lambda: self.router.get("/", response_model=list[model])(self.find_all),
            self.find_by_id.__name__: lambda: self.router.get("/{id}", response_model=model)(self.find_by_id),
            self.update.__name__: lambda: self.router.put("/{id}", response_model=model)(self.update),
            self.delete.__name__: lambda: self.router.delete("/{id}")(self.delete),
        }

        routes_could_define = {key: value for key, value in routes_define.items() if key not in exclude}

        for define in routes_could_define.values():
            define()

    def delete_query(self, path: str,
                     router: APIRouter | None = None,
                     method: HTTPMethod | None = None,
                     name: str | None = None):
        """

        :param name:
        :param method:
        :param router:
        :param path: Template: prefix/{path}/
        :return:
        :Example:
        Example::

            router = crud_router.delete_query('items', router, name=get_items_v1.__name__)
        """
        if router is None:
            router = self.router
        if len(path) > 0:
            if path[0] == '/':
                path = path[1:]
        logging.debug(f"Routes was: {router.routes}")
        router.routes = [
            r for r in router.routes
            if not (isinstance(r, APIRoute)
                    and r.path == f"{self.prefix}/{path}"
                    and (method is None or r.methods == [method.value])
                    and (name is None or r.name == name))
        ]
        logging.getLogger(__name__)
        logging.debug(f"Routes now: {router.routes}")
        if router is None:
            self.router = router
        return router

    def _create(self, schema_type: CreateSchemaT | ModelT):
        async def create(item: schema_type):
            obj: type[ModelT] = self.model(**item.model_dump())
            await obj.insert()
            return obj

        return create

    def _update(self, schema_type: UpdateSchemaT | ModelT):
        async def update(id: PydanticObjectId, item: schema_type):
            obj = await self.model.get(id)
            if not obj:
                raise HTTPException(status_code=404, detail="Not found")
            update_data = {k: v for k, v in item.model_dump(exclude_unset=True).items()}
            update_data['update_at'] = datetime.now()
            await obj.set(update_data)
            return await self.model.get(id)

        return update

    async def find_all(self):
        return await self.model.find_all().to_list()

    async def find_by_id(self, id: PydanticObjectId):
        obj = await self.model.get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj

    async def delete(self, id: PydanticObjectId):
        obj = await self.model.get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        await obj.delete()
        return {"ok": True}
