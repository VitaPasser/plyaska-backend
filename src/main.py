import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.utils.config import settings
from src.utils.controllers.controllers_loader import load_fastapi_routers
from src.utils.db.mongo_db_provider import MongoDBProvider
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
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await self.setup()
            yield
            await self.teardown()

        self.app = FastAPI(lifespan=lifespan)
        self.app = include_exceptions(self.app)
        logging.info("Main initialized")

    async def setup(self):
        await self._db.connect()
        logging.info("Loading routers...")
        for router in load_fastapi_routers("src.controllers"):
            self.app.include_router(router)
        logging.info("Routers loaded")
        return self

    async def teardown(self):
        await self._db.disconnect()
        print("Main down...")


main = Main()

if __name__ == "__main__":
    uvicorn.run(
        "src.main:main.app",
        host=(os.getenv("SERVER_INTERNAL_HOST") or "0.0.0.0"),
        port=(int(os.getenv("SERVER_INTERNAL_PORT") or 8000)),
        reload=True,
    )
