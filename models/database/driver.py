'''

    Here is all CRUD operations for database
    Must be implemented from IDatabaseDriver

'''

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .idatabase_driver import IDatabaseDriver

import sqlalchemy
from sqlalchemy import create_engine, insert

from .tables import *



def checkConnection(func):
    def wrapper(self, *args, **kwargs):
        if not self.getCurrentSession(): return

        return func(self, *args, **kwargs)

    return wrapper



class Driver(IDatabaseDriver):
    def __init__(self):
        self.__engine = create_engine('sqlite:///sqlite3.db')
        self.__engine.connect()

        createTables(self.__engine)

        self.__session = sessionmaker(bind=self.__engine)()

    def getCurrentSession(self): return self.__session

    @checkConnection
    def save(self):
        self.__session.commit()

    @checkConnection
    def create(self, mailName: str, commit=True):
        mail = Mail( mail=mailName )
        self.__session.add(mail)

        if commit: self.save()

    @checkConnection
    def getMailCount(self):
        return self.__session.query(Mail).count()

    @checkConnection
    def read(self, ID=None, MAIL=None) -> list|Mail:
        allObjects = self.__session.query(Mail)

        if not ID is None: return allObjects.get(ID)
        if not MAIL is None: return allObjects.filter(Mail.mail == MAIL)[0]
        return allObjects.all()


    @checkConnection
    def update(self):
        pass

    @checkConnection
    def delete(self, _id: int):
        self.__session.delete(
            self.read(ID=_id)
        )