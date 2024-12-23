from .connection import Connection, checkConnection


class Driver:
    __session = None

    def __init__(self):
        self.__session = Connection().createSession()

    # for connection checker
    def getCurrentSession(self): return self.__session

    @checkConnection
    def save(self):
        self.__session.commit()
