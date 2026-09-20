import json
from PySide6.QtWidgets import QMessageBox

class Settings(object):
    def __init__(self):
        self.default_settings: dict = {
            'general': {'lang': {'en': True, 'pl': False},
                        'theme': {'sys': True, 'dark': False, 'light': False},
                        'save_on_stop': True},
            'key_bindings': {'start_recording': 'ctrl+a', 'stop_recording': 'ctrl+s'}}

        self.user_prefs: dict = self.load_settings()

    def get_all_settings(self):
        return self.user_prefs

    def load_settings(self) -> dict:
        try:
            with open('user_prefs.json', 'r') as config_file:
                data = json.load(config_file)
                return data
        except FileNotFoundError:
            error_reason:str = 'user_prefs.json not found'
            QMessageBox.warning(None,'Error', f'Error loading user_prefs.json. {error_reason}. '
                                         f'Loading default settings.)')
            return self.default_settings
        except json.decoder.JSONDecodeError:
            error_reason:str = 'Error loading user_prefs.json. Json decode error.'
            QMessageBox.warning(None, 'Error', f'Error loading user_prefs.json. {error_reason}. '
                                               f'Loading default settings.)')
            return self.default_settings

    def save_settings(self, data: dict) -> None:
        config_json = json.dumps(data)
        with open('user_prefs.json', 'w') as config_file:
            config_file.write(config_json)

    def get_default_settings(self) -> dict:
        return self.default_settings

    @staticmethod
    def is_settings_loaded(prefs:dict) -> bool:
        if not prefs:
            return False
        else:
            return True

    def get_setting(self, key):
        pass
