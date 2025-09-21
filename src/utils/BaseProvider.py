import logging
from abc import ABC


class BaseProvider(ABC):
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        super().__init__()