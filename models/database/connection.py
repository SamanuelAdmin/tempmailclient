from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .tables import *


# will be a singleton
class Connection:
    classObject = None
    __engine = None
    __session = None

    def __new__(cls):
        if cls.classObject is None:
            cls.classObject = super(Connection, cls).__new__(cls)
            cls.connectToEngine()
            createTables(cls.__engine)
            cls.__session = Session(bind=cls.__engine)

        return cls.classObject


    @classmethod
    def connectToEngine(cls):
        cls.__engine = create_engine('sqlite:///sqlite3.db')
        cls.__engine.connect()

    def createSession(self):
        return self.__session


def checkConnection(func):
    def wrapper(self, *args, **kwargs):
        if not self.getCurrentSession(): return

        return func(self, *args, **kwargs)

    return wrapper