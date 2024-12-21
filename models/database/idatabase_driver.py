from abc import ABC, abstractmethod

class IDatabaseDriver(ABC):
    @abstractmethod
    def save(self): pass

    # CRUD
    @abstractmethod
    def create(self): pass

    @abstractmethod
    def read(self): pass

    @abstractmethod
    def update(self): pass

    @abstractmethod
    def delete(self): pass