'''

TEMP MAIL API
API for the https://www.1secmail.com/api/ service

'''
from os.path import split

import requests
from fake_useragent import UserAgent
import urllib

import random


API_URL = 'https://www.1secmail.com/api/v1/'

class FakeUserAgent(UserAgent):
    def __init__(self, browsers=None):
        if browsers is None:
            browsers = [
                "Google",
                "Chrome",
                "Firefox",
                "Edge",
                "Opera",
                "Safari",
                "Android",
                "Yandex Browser",
                "Samsung Internet",
                "Opera Mobile",
                "Mobile Safari",
                "Firefox Mobile",
                "Firefox iOS",
                "Chrome Mobile",
                "Chrome Mobile iOS",
                "Mobile Safari UI/WKWebView",
                "Edge Mobile",
                "DuckDuckGo Mobile",
                "MiuiBrowser",
                "Whale",
                "Twitter",
                "Facebook",
                "Amazon Silk"
            ]

        super().__init__(browsers=browsers)

    def get(self): return self.random


class TempMailClient:
    # https://www.1secmail.com/api/

    def __init__(self):
        self.fakeUserAgent = FakeUserAgent()
        self.proxies: list[dict[str, str]] = []

    def addProxy(self,
                     host: str, port: int,
                     username: str|None=None, password: str="",
                     methods: list[str]=["http", "https"]
                 ) -> None:
        proxy = dict()

        for method in methods:
            proxy[method] = f'{method}://{str(username) + ":" + str(password) + "@" if username else ""}{host}:{port}'

        self.proxies.append(proxy)


    def addSystemProxy(self):
        self.proxies.append(urllib.request.getproxies())


    def getRandomProxy(self):
        return random.choice(self.proxies)

    def apiRequest(self, proxy=None, **kwargs) -> dict|int:
        headers = {
            'user-agent': self.fakeUserAgent.get(),
        }

        params = dict()
        for key, value in kwargs.items():
            params[key] = str(value)

        if not proxy and self.proxies != []:
            proxy = self.getRandomProxy() if not proxy else proxy

        request = requests.get(
            API_URL,
            params=params,
            headers=headers,
            proxies=proxy
        )

        if request.status_code == 200:
            return request.json()
        return request.status_code

    def getRandomMail(self, count=1) -> list[str]|str:
        # https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=10

        r = self.apiRequest(action="genRandomMailbox", count=count)

        if type(r) == int: # if it is something to return
            return []
        return r if len(r) > 1 else r[0]

    def checkMailbox(self, mail: str) -> list[dict]:
        # https://www.1secmail.com/api/v1/?action=getMessages&login=demo&domain=1secmail.com
        username, domain = mail.split('@')

        r = self.apiRequest(action="getMessages", login=username, domain=domain)

        if type(r) == int: return []
        return r

    def readMessage(self, mail: str, emailId: int) -> dict:
        # https://www.1secmail.com/api/v1/?action=readMessage&login=demo&domain=1secmail.com&id=639
        username, domain = mail.split('@')

        r = self.apiRequest(action="readMessage", login=username, domain=domain, id=emailId)

        if type(r) == int: return {}
        return r


if __name__ == '__main__':
    # FOR TEST ONLY

    tms = TempMailClient()

    print(tms.checkMailbox('2v1a9znqlt@1secmail.com'))
