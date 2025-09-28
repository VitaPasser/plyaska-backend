import logging
import os
import posixpath
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from src.utils.handlers.exceptionHandlers import ExceptionHandlers
from src.utils.Logging import logging_setup
from src.utils.controllers.ControllersLoader import load_fastapi_routers
from src.utils.db.MongoDBProvider import MongoDBProvider

load_dotenv(f"{posixpath.dirname(__file__)}/../.env")

class Main:
    def __init__(self):
        logging_setup()
        logging.info("Starting main initialization...")
        self._db = MongoDBProvider(database="plyaska_db",
                                   username=os.getenv("MONGO_USERNAME"),
                                   password=os.getenv("MONGO_PASSWORD"),
                                   host=os.getenv("MONGO_HOST"), )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await self.setup()
            yield
            await self.teardown()
        self.app = FastAPI(lifespan=lifespan)
        eh = ExceptionHandlers()
        self.app.add_exception_handler(Exception, eh.unhandled_exception_handler)
        self.app.add_exception_handler(HTTPException, eh.http_exception_handler)
        logging.info("Main initialized")

    async def setup(self):
        await self._db.connect()
        logging.info("Loading routers...")
        for router in load_fastapi_routers('src.controllers'):
            self.app.include_router(router)
        logging.info("Routers loaded")
        return self

    async def teardown(self):
        await self._db.disconnect()
        print("Main down...")


main = Main()

if __name__ == "__main__":
    uvicorn.run("src.main:main.app",
                host=(os.getenv("SERVER_INTERNAL_HOST") or "0.0.0.0"),
                port=(int(os.getenv("SERVER_INTERNAL_PORT") or 8000)),
                reload=True)
