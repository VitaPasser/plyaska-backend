from functools import wraps
from typing import Callable

from fastapi import APIRouter


@wraps(APIRouter.api_route)
def route(**router_kwargs):
    def decorator(func: Callable):
        func._route_info = {
            "kwargs": router_kwargs
        }
        return func
    return decorator

@wraps(APIRouter.get)
def get(path: str, **kwargs): return route(methods=["GET"], path=path, **kwargs)
@wraps(APIRouter.post)
def post(path: str, **kwargs): return route(methods=["POST"], path=path, **kwargs)
@wraps(APIRouter.put)
def put(path: str, **kwargs): return route(methods=["PUT"], path=path, **kwargs)
@wraps(APIRouter.delete)
def delete(path: str, **kwargs): return route(methods=["DELETE"], path=path, **kwargs)
@wraps(APIRouter.patch)
def patch(path: str, **kwargs): return route(methods=["PATCH"], path=path, **kwargs)

def register_routes(cls):
    orig_init = cls.__init__

    def __init__(self, *args, **kwargs):
        orig_init(self, *args, **kwargs)

        if not hasattr(self, "router"):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'router'")

        for name, method in cls.__dict__.items():
            info = getattr(method, "_route_info", None)
            if info:
                self.router.add_api_route(
                    endpoint=getattr(self, name),
                    **info["kwargs"]
                )
    cls.__init__ = __init__
    return cls