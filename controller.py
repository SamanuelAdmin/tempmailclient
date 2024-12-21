# its a controller (from MVC pattern)

from itertools import chain # for list building

from flask import request, Response, redirect

from models.mail_api_client import TempMailClient
from views.view import View
from models.database.driver import Driver

# settings import
from settings import *


class Email:
    def __init__(self, mail, emailData):
        self.ID = emailData['id']
        self.frommail = emailData['from']
        self.subject = emailData['subject']
        self.date = emailData['date']

        self.login, self.domain = mail.split('@')


class Controller:
    def __init__(self, app):
        self.__app = app
        self.view = View()

        self.tempMailClient = TempMailClient()
        self.databaseDriver = Driver()

    def router(self):
        @self.__app.route('/')
        def index():
            mailList = self.databaseDriver.read()

            # filters for emails
            mailFilter = request.args.get('from')

            if mailFilter:
                emailsList = [Email(mailFilter, data) for data in self.tempMailClient.checkMailbox(mailFilter)]
            else:
                emailsList = list(
                    chain.from_iterable(
                        [Email(mail.mail, data) for data in self.tempMailClient.checkMailbox(mail.mail)] for mail in mailList
                    )
                )


            return self.view.index(mailList, emailsList, choosen=mailFilter)

        @self.__app.route('/read')
        def readPage():
            mailList = self.databaseDriver.read()

            mail = request.args.get('mail')
            emailId = request.args.get('id')

            if not mail or not emailId:
                return redirect('/')

            emailDetails = self.tempMailClient.readMessage(mail, int(emailId))
            email2read = Email( mail, emailDetails )

            return self.view.index(mailList, [], email2read=email2read)

        @self.__app.route('/addmail')
        def addMail():
            mail = self.tempMailClient.getRandomMail(count=1)
            self.databaseDriver.create(mail)

            return Response(status=200)

        @self.__app.route('/deletemail')
        def deleteMail():
            mail = request.args.get('mail')

            self.databaseDriver.delete(
                self.databaseDriver.read(MAIL=mail).id
            )

            return Response(status=200)