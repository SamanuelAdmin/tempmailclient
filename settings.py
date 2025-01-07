import os

from models.config_manager.manager import UserConfigsManager


ROOT_DIR = os.getcwd()

USER_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, 'user_configs.json')

# user configs manager
# THE ONLY CORRECT WAY TO GET USER CONFIG IS UserConfigsManager.getUserConfig('name')
userConfigsManager = UserConfigsManager()
userConfigsManager.init(USER_CONFIG_FILE_PATH, autoLoad=True)


APP_CONFIGS = {
    'host': UserConfigsManager.getUserConfig('host'),
    'port': UserConfigsManager.getUserConfig('port')
}


UPDATE_TIMEOUT = 30 # timeout before every email database update