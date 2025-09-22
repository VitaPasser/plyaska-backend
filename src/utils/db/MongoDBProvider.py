import logging
from beanie import init_beanie
from pymongo import AsyncMongoClient

from src.utils.db.DBProvider import DBProvider
from src.utils.models.ModelsLoader import load_beanie_models


def _load_documents():
    return load_beanie_models("src.models")


class MongoDBProvider(DBProvider):
    __is_initialized: bool = False
    __client: AsyncMongoClient|None = None

    def __init__(self, database: str, username: str, password: str, host: str):
        self.username = username
        self.password = password
        self.host = host
        self.db = database
        super().__init__()

    def __get_url(self) -> str:
        return f"mongodb://{self.username}:{self.password}@{self.host}:27017"

    async def connect(self):
        if not self.__client:
            self.__client = AsyncMongoClient(self.__get_url())
            logging.info("Connected to MongoDB")
        if not self.__is_initialized:
            loaded_documents = _load_documents()
            logging.debug(f"Loaded documents: {loaded_documents}")
            await init_beanie(database=self.__client.plyaska_db,
                              document_models=loaded_documents)
            self.__is_initialized = True
            logging.info("DB is initialized with Beanie")

        return self.__client

    def get_client(self) -> AsyncMongoClient:
        return self.__client

    async def disconnect(self):
        if not self.__client:
            self.__is_initialized = False
            logging.info("DB was been disconnected")
            return
        await self.__client.close()
        self.__client = None
        self.__is_initialized = False
        logging.info("DB is disconnected")

