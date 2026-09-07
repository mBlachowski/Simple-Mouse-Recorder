import json



class Settings(object):
    def __init__(self):
        self.default_settings: dict = {
            'general': {'lang': {'en':True, 'pl':False},
            'theme': {'sys':True, 'dark':False, 'light': False},
            'save_on_stop': True},
            'key_bindings': {'start_recording': '','stop_recording': ''}}

        self.user_prefs:dict = self.load_settings()

        if not self.is_settings_loaded():
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(None, 'Load error',
                                    'Error while loading user_prefs.json. Loading default settings.')
            self.user_prefs = self.default_settings
            self.save_settings()

    def get_all_settings(self):
        return self.user_prefs

    def load_settings(self) -> dict:
        try:
            with open('user_prefs.json', 'r') as config_file:
                data = json.load(config_file)
                return data
        except FileNotFoundError:
            print('Error while loading user_prefs.json. No such file or directory.')
            return {}
        except json.decoder.JSONDecodeError:
            print('Error while loading user_prefs.json. Json decode error.')
            return {}


    def save_settings(self):
        config_json = json.dumps(self.user_prefs)
        with open('user_prefs.json', 'w') as config_file:
            config_file.write(config_json)

    def get_default_settings(self) -> dict:
        return self.default_settings

    def is_settings_loaded(self) -> bool:
        if not self.user_prefs:
            return False
        else:
            return True

    def get_setting(self, key):
        pass