from flask import Flask

from settings import APP_CONFIGS
from controller import Controller


class MainApp(Flask):
    def __init__(self, **kwargs):
        super().__init__("main", **kwargs)

        controller = Controller(self)
        controller.router()


if __name__ == '__main__':
    # only for tests
    MainApp(**APP_CONFIGS).run()