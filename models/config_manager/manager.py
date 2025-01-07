import json
from datetime import datetime

from django.db.models import Manager
from django.db.models.expressions import result
from sqlalchemy.testing.suite.test_reflection import users


def json2StringFormate(jsonInDict: dict, separator: str="   ") -> str:
    '''
        strJson = '{"key1": "value1", "key2": "value2", "key3": {"key4": "value4", "key5": "value5"}}'
        Output:
            {
                "key1": "value1",
                "key2": "value2",
                "key3": {
                    "key4": "value4",
                    "key5": "value5"
                }
            }
    '''

    result = ''
    paddingCount = 0

    def addLayer(obj: dict, result, paddingCount, isLastItem) -> None:
        result += '{'
        paddingCount += 1

        for key, value in obj.items():
            if isinstance(value, list):
                result += f'\n{separator * paddingCount}"{key}": ['
                paddingCount += 1
                for item in value:
                    if isinstance(item, str): item = f'"{item}"'

                    result += f'\n{separator * paddingCount}{item}{"," if item != value[-1] else ""}'
                paddingCount -= 1
                result += f'\n{separator * paddingCount}]{"," if key != list(obj.keys())[-1] else ""}'

            elif isinstance(value, dict):
                result += f'\n{separator * paddingCount}"{key}": '
                result, paddingCount = addLayer(value, result, paddingCount, key == list(obj.keys())[-1])

            else:
                if isinstance(value, str):
                    value = f'"{value}"'

                result += f'\n{separator * paddingCount}"{key}": {value}{"," if key != list(obj.keys())[-1] else ""}'

        paddingCount -= 1
        result += '\n' + str(separator * paddingCount) + '}' + str('' if isLastItem else ',')

        return result, paddingCount

    result, paddingCount = addLayer(jsonInDict, result, paddingCount, True)

    return result




class EmptyConfigsException(Exception):
    pass


def checkConfigsIsEmpty(configs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if configs != {}:
                return func(*args, **kwargs)
            else: raise EmptyConfigsException()

        return wrapper

    return decorator



class UserConfigsManager:
    __configFilePath = ''
    __configs = {}
    __cls = None

    def __new__(cls, *args, **kwargs): # make this class singleton
        if cls.__cls is None: # first build
            cls.__cls = super().__new__(cls)

        return cls.__cls

    def __init__(self, configFilePath, autoLoad=False):
        self.__configFilePath = configFilePath

        if autoLoad:
            self.loadUserConfigs()


    @classmethod
    def loadUserConfigs(cls):
        with open(cls.__configFilePath, "r") as configsString:
            try: cls.__configs = json.load(configsString)
            except Exception as err:
                print(f'[{str(datetime.now())[:-7]}] Cannot load user configs from JSON file {cls.__configFilePath} by \n{err}')

    @classmethod
    @checkConfigsIsEmpty(__configs)
    def saveUserConfigs(cls):
        formatedConfigString = json2StringFormate(cls.__configs)

        with open(cls.__configFilePath, "w") as configsFile:
            configsFile.write(formatedConfigString)

        print(f'[{str(datetime.now())[:-7]}] User configs has been saved.')

    @classmethod
    @checkConfigsIsEmpty(__configs)
    def getUserConfig(cls, name: str) -> str|int|dict|list:
        return cls.__configs.get(name)

    @classmethod
    @checkConfigsIsEmpty(__configs)
    def setUserConfig(cls, name: str, value: str|int|dict|list) -> None:
        print(f'[{str(datetime.now())[:-7]}] Set/change user config [{name}] to {value}')
        cls.__configs[name] = value



# test formatter and UserConfigsManager
if __name__ == '__main__':
    # testDict = {
    #     'key1': 'value1',
    #     'key2': 235345,
    #     'key3': {
    #         'key4': 'value4',
    #         'key5': 'value5',
    #         'key6': {
    #             'key7': 'value7',
    #             'key8': 'value8',
    #         },
    #         'key9': [1, 2, 3, 4],
    #         'key10': 'test'
    #     }
    # }
    #
    # print(
    #     json2StringFormate(
    #         testDict,
    #     )
    # )

    # singleton test
    ucm1 = UserConfigsManager('')
    ucm2 = UserConfigsManager('')

    if id(ucm1) == id(ucm2): print('Class is singleton')

    ucm1._UserConfigsManager__configs = {'some': 1}
    ucm1.setUserConfig('test', True)

    print(
        UserConfigsManager.getUserConfig('test')
    )
