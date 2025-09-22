import logging
from abc import abstractmethod

from src.utils.BaseProvider import BaseProvider


class DBProvider(BaseProvider):
    def __init__(self):
        super().__init__(logging.getLogger(__name__))

    @abstractmethod
    def connect(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError("Subclasses must implement this method")