from flask import render_template


class View:
    def __int__(self): pass

    def index(self, mailList, emailList, choosen=None, email2read=None):
        return render_template(
            'index.html',
            title="TempMail Client",
            emailList = emailList,
            emailsCount=len(emailList),
            mailList = mailList,
            mailsCount=len(mailList),
            choosen=choosen,
            email2read=email2read
        )