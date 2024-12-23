from .connection import checkConnection
from .driver import Driver
from .idatabase_driver import IDatabaseDriver

from .tables import *



class EmailDriver(Driver, IDatabaseDriver):
    def __init__(self):
        super().__init__()

    @checkConnection
    def create(self, email, commit=True):
        newEmail = Email(
            int(email.emailId),
            email.frommail,
            email.subject,
            email.date,
            email.htmlBody,
            email.login, email.domain
        )

        self.getCurrentSession().add(newEmail)
        if commit: self.save()

    @checkConnection
    def read(self, id=None, emailId=None, condition=None) -> list | Mail|None:
        allObjects = self.getCurrentSession().query(Email)

        if not condition is None: return allObjects.filter(condition).first()
        if not id is None: return allObjects.get(id)
        if not emailId is None: return allObjects.filter_by(emailId = emailId).first()
        return allObjects.order_by(Email.date.desc()).all()  # new one will be at the beginning

    def update(self):
        pass

    @checkConnection
    def delete(self, _id: int):
        self.getCurrentSession().delete(
            self.read(emailId=_id)
        )
        self.getCurrentSession().commit()

