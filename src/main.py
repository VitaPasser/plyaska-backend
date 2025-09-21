import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException

from src.exceptionHandlers import ExceptionHandlers
from src.providers import provider_register
from src.utils.Logging import logging_setup
from src.utils.db.MongoDBProvider import MongoDBProvider


class Main:
    def __init__(self):
        self._logger = logging_setup()
        self._logger.info("Starting main initialization...")
        self._db = MongoDBProvider(self._logger,
                                   database="plyaska_db",
                                   username=os.getenv("MONGO_USERNAME"),
                                   password=os.getenv("MONGO_PASSWORD"),
                                   host=os.getenv("MONGO_HOST"), )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await self.setup()
            yield
            await self.teardown()

        self.app = FastAPI(lifespan=lifespan)
        eh = ExceptionHandlers(self._logger)
        self.app.add_exception_handler(Exception, eh.unhandled_exception_handler)
        self.app.add_exception_handler(HTTPException, eh.http_exception_handler)
        self._logger.info("Main initialized")

    async def setup(self):
        await self._db.connect()
        self._logger.info("Loading providers...")
        for provider in provider_register(self._logger, self._db):
            self.app.include_router(provider.router)
        self._logger.info("Providers loaded")
        return self

    async def teardown(self):
        await self._db.disconnect()
        print("Main down...")


main = Main()

if __name__ == "__main__":
    uvicorn.run("src.main:main.app",
                host=(os.getenv("SERVER_INTERNAL_HOST")),
                port=(int(os.getenv("SERVER_INTERNAL_PORT"))),
                reload=True)
