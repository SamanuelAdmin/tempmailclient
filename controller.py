# its a controller (from MVC pattern)
import threading
import time
from io import BytesIO

from sqlalchemy import and_

from flask import request, Response, redirect, send_file

from models.mail_api_client import TempMailClient
from views.view import View
from models.database.mail_driver import MailDriver
from models.database.email_driver import EmailDriver
from models.email_description import EmailDesc

from models.database.tables import *

# settings import
from settings import *


class Controller:
    def __init__(self, app):
        self.__app = app
        self.view = View()

        self.tempMailClient = TempMailClient()
        self.mailDriver = MailDriver()
        self.emailDriver = EmailDriver()

        threading.Thread(
            target=self.updateEmailData, daemon=True
        ).start()


    def updateEmailData(self, timeout=UPDATE_TIMEOUT):
        while True:
            mailList = self.mailDriver.read()

            for mail in mailList:
                for emailBoxData in self.tempMailClient.checkMailbox(mail.mail):
                    emailId = emailBoxData.get('id')
                    if emailId is None: continue

                    if self.emailDriver.read(emailId=emailId) is None: # if it is new email
                        emailData = self.tempMailClient.readMessage(mail.mail, int(emailId))
                        email = EmailDesc(mail.mail, emailData)

                        print(f'Saving new email with ID {email.emailId}.')
                        self.emailDriver.create(email)

            time.sleep(timeout)



    def router(self):
        @self.__app.route('/')
        def index():
            mailList = self.mailDriver.read()
            emailsList = self.emailDriver.read()

            return self.view.index(mailList, emailsList)


        @self.__app.route('/email/download')
        def downloadEmail():
            mail = request.args.get('mail')
            emailId = request.args.get('id')

            if emailId is None or mail is None:
                return Response(status=400)


            email = self.emailDriver.read(
                condition=and_(
                    Email.emailId == emailId, Email.login + '@' + Email.domain == mail
                )
            )

            if email is None: return Response(status=404)

            emailPage = self.view.getEmailTemplate(
                self.__app.jinja_env, email
            )

            return send_file(
                BytesIO(emailPage.encode('utf-8')),
                as_attachment=True,
                download_name=f"email {email.emailId}.html"
            )


        @self.__app.route('/mail/add', methods=['POST'])
        def addMail():
            mail = self.tempMailClient.getRandomMail(count=1)

            if type(mail) == list:
                return Response(status=502)

            self.mailDriver.create(mail)

            return Response(status=200)

        @self.__app.route('/mail/delete', methods=['POST'])
        def deleteMail():
            mail = request.args.get('mail')

            if mail == 'all':
                for mail in self.mailDriver.read():
                    self.mailDriver.delete(mail.id)
            else:
                if mail is None: return Response(status=400)

                self.mailDriver.delete(
                    self.mailDriver.read(MAIL=mail).id
                )

            return Response(status=200)

        @self.__app.route('/email/delete', methods=['POST'])
        def deleteEmail():
            emailId = request.args.get('id')

            if emailId is None: return Response(status=400)

            self.emailDriver.delete(int(emailId))

            return Response(status=200)



