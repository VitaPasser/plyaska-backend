from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware


def add_middlewares(app: FastAPI):
    middlewares = [PrometheusMiddleware]

    for middleware in middlewares:
        app.add_middleware(middleware)

    return app
