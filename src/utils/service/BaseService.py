from logging import Logger
from abc import ABC

from src.utils.db.DBProvider import DBProvider


class BaseService(ABC):
    def __init__(self, logger: Logger, database: DBProvider):
        self._logger = logger
        self._db = database
        super().__init__()