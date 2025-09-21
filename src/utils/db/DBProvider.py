from abc import abstractmethod

from src.utils.BaseProvider import BaseProvider


class DBProvider(BaseProvider):
    def __init__(self, logger):
        super().__init__(logger)

    @abstractmethod
    def connect(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError("Subclasses must implement this method")