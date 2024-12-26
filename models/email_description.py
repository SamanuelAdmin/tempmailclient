class EmailDesc:
    def __init__(self, mail: str, emailData: dict[str, str]):
        self.emailId = emailData['id']
        self.frommail = emailData['from']
        self.subject = emailData['subject']
        self.date = emailData['date']

        self.textBody = emailData.get('textBody')
        self.htmlBody = emailData.get('htmlBody')
        self.body = emailData.get('body')

        self.login, self.domain = mail.split('@')
