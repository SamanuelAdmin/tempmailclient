from .connection import checkConnection
from .driver import Driver
from .idatabase_driver import IDatabaseDriver

from .tables import *


class MailDriver(Driver, IDatabaseDriver):
    def __init__(self):
        super().__init__()


    @checkConnection
    def create(self, mailName: str, commit=True):
        mail = Mail( mail=mailName )
        self.getCurrentSession().add(mail)

        if commit: self.save()

    @checkConnection
    def getMailCount(self):
        return self.getCurrentSession().query(Mail).count()

    @checkConnection
    def read(self, ID=None, MAIL=None) -> list|Mail:
        allObjects = self.getCurrentSession().query(Mail)

        if not ID is None: return allObjects.get(ID)
        if not MAIL is None: return allObjects.filter(Mail.mail == MAIL)[0]
        return allObjects.all()


    @checkConnection
    def update(self):
        pass

    @checkConnection
    def delete(self, _id: int):
        self.getCurrentSession().delete(
            self.read(ID=_id)
        )
        self.getCurrentSession().commit()