from fastapi import APIRouter

from src.utils.controller.RoutesUtils import register_routes


@register_routes
class BaseController:
    router: APIRouter = APIRouter()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        register_routes(cls)