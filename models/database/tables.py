from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, \
    Numeric, PrimaryKeyConstraint, \
    UniqueConstraint, Index, CheckConstraint

from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Mail(Base):
    __tablename__ = 'mail'
    id = Column(Integer, primary_key=True)
    mail = Column(String(70), nullable=False)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('mail'),
    )

class Email(Base):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)

    # email id (from api)
    emailId = Column(Integer, nullable=False)
    frommail = Column(String(100), nullable=False)
    subject = Column(String(500), nullable=False)
    date = Column(DateTime, nullable=True)

    body = Column(String, nullable=True)

    # addressee mail (format: login@domain)
    login = Column(String, nullable=False)
    domain = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('emailId'),
        Index('ix_date', 'date'),
        Index('ix_from_mail', 'frommail'),
        Index('ix_subject', 'subject'),
        Index('ix_body', 'body'),

        Index('ix_email_login', 'login'),
        Index('ix_email_domain', 'domain'),
    )

    def __init__(
            self, emailId: int,
            frommail: str, subject: str,
            date: str,
            body: str,
            login: str, domain: str):

        self.emailId = emailId
        self.frommail = frommail
        self.subject = subject
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
        self.body = body
        self.login = login
        self.domain = domain




def createTables(engine):
    Base.metadata.create_all(engine)