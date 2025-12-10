import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from setuptools._distutils.util import strtobool

from src.utils.config import settings
from src.utils.controllers.controllers_loader import load_fastapi_routers
from src.utils.db.mongo_db_provider import MongoDBProvider
from src.utils.db.redis_db_provider import RedisDBProvider
from src.utils.handlers.exception_handlers import include_exceptions
from src.utils.logging import logging_setup


class Main:
    def __init__(self) -> None:
        logging_setup()
        logging.info("Starting main initialization...")
        env = settings
        self._db = MongoDBProvider(
            database="plyaska_db",
            username=env.mongo_username,
            password=env.mongo_password,
            host=env.mongo_host,
            port=env.mongo_port,
        )
        self._cache = RedisDBProvider(
            host=env.redis_host,
            port=env.redis_port,
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await self.setup()
            yield
            await self.teardown()

        self.app = FastAPI(lifespan=lifespan)
        self.app = include_exceptions(self.app)
        logging.info("Main initialized")

    async def get_connect_cache(self):
        return await self._cache.connect()

    async def setup(self):
        await self._db.connect()
        await self._cache.connect()
        logging.info("Loading routers...")
        for router in load_fastapi_routers("src.controllers"):
            self.app.include_router(router)
        logging.info("Routers loaded")
        return self

    async def teardown(self):
        await self._db.disconnect()
        await self._cache.disconnect()
        print("Main down...")


main = Main()


def start_server():
    try:
        port = int(os.getenv("SERVER_INTERNAL_PORT"))
    except:
        port = settings.server_internal_port or 8000

    try:
        reload = os.getenv("SERVER_HOT_RELOADED_ON")
        reload = bool(strtobool(reload))
    except (AttributeError,ValueError):
        reload = bool(strtobool(settings.server_hot_reloaded_on or False))

    try:
        workers = int(os.getenv("SERVER_COUNT_WORKERS"))
    except:
        workers = settings.server_count_workers or 1

    logging.debug(f"workers count: {workers}")
    uvicorn.run(
        "src.main:main.app",
        host=(os.getenv("SERVER_INTERNAL_HOST") or settings.server_internal_host or "0.0.0.0"),
        port=port,
        reload=reload,
        workers=workers,
        timeout_keep_alive=10,
    )


if __name__ == "__main__":
    start_server()
