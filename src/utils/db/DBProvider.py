from abc import abstractmethod, ABC


class DBProvider(ABC):
    @abstractmethod
    def connect(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError("Subclasses must implement this method")