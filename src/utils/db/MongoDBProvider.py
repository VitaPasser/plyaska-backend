from beanie import init_beanie
from pymongo import AsyncMongoClient

from src.utils.db.DBProvider import DBProvider
from src.utils.db.ModelsLoader import load_beanie_models


def _load_documents():
    return load_beanie_models("src.models")


class MongoDBProvider(DBProvider):
    __is_initialized: bool = False
    __client: AsyncMongoClient|None = None

    def __init__(self, logger, database: str, username: str, password: str, host: str):
        self.username = username
        self.password = password
        self.host = host
        self.db = database
        super().__init__(logger)

    def __get_url(self) -> str:
        return f"mongodb://{self.username}:{self.password}@{self.host}:27017"

    async def connect(self):
        if not self.__client:
            self.__client = AsyncMongoClient(self.__get_url())
            self._logger.info("Connected to MongoDB")
        if not self.__is_initialized:
            await init_beanie(database=self.__client.plyaska_db,
                              document_models=_load_documents())
            self.__is_initialized = True
            self._logger.info("DB is initialized with Beanie")

        return self.__client

    def get_client(self) -> AsyncMongoClient:
        return self.__client

    async def disconnect(self):
        if not self.__client:
            self.__is_initialized = False
            self._logger.info("DB was been disconnected")
            return
        await self.__client.close()
        self.__client = None
        self.__is_initialized = False
        self._logger.info("DB is disconnected")

