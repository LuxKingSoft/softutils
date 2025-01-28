#  Copyright (c) 2024.
#  Creation Date: 2024-8-20
#  Author: Lux King Soft

"""
This module defines a Settings class which loads the settings for the bot.
Use a dot notation as separator to find settings nested settings.

For example:
"server_settings.port" will access the "port" specified of "server_settings".

Here are also defined two exception classes used in Settings.
"""

import json

import toml


class SettingNotFoundError(Exception):
    """Exception class that is raised when the setting specified is not found"""

    def __init__(self, msg=""):
        super().__init__(msg)


class FileNotWellFormatted(Exception):
    """Exception class that is raised when the specified file is not well formatted"""

    def __init__(self, msg=""):
        super().__init__(msg)


class Settings:
    """These are the supported configuration file formats."""
    SETTINGS_FILE_TYPE_TOML = "toml"
    SETTINGS_FILE_TYPE_JSON = "json"

    # These are the actions that can be performed through the configuration dictionary
    _ACCESS_ACTION_ADD = 0x01
    _ACCESS_ACTION_READ = 0x02
    _ACCESS_ACTION_REMOVE = 0x03
    _ACCESS_ACTION_UPDATE = 0x04

    def __init__(self, file, file_type):
        self.settings_file = file
        self.settings_file_type = file_type
        self._all_settings = {}

    @property
    def all_settings(self):
        return self._all_settings

    @all_settings.setter
    def all_settings(self, dictionary):
        self._all_settings = dictionary

    def load_from_file(self, path):
        """Load settings from the specified configuration file."""
        try:
            if self.settings_file_type == self.SETTINGS_FILE_TYPE_TOML:
                self._all_settings = self._load_toml(path)
            elif self.settings_file_type == self.SETTINGS_FILE_TYPE_JSON:
                self._all_settings = self._load_json(path)
        except json.JSONDecodeError as e:
            raise FileNotWellFormatted("The JSON file specified is not well formatted. " + str(e))
        except toml.TomlDecodeError as e:
            raise FileNotWellFormatted("The TOML file specified is not well formatted. " + str(e))

    @staticmethod
    def _load_json(path):
        data = {}
        with open(path, "r") as f:
            data.update(json.load(f))
        return data

    @staticmethod
    def _load_toml(path):
        data = {}
        with open(path, "r", encoding="utf-8") as f:
            data.update(toml.load(f))
        return data

    def _access_setting(self, setting: str, value="", action=_ACCESS_ACTION_READ):
        """
        This method recursively finds the key the user refers to and reads, writes, or deletes the key-value
        pair. Returns the setting(s) requested by the user or all configurations with the updated settings.
        """
        keys = setting.split(".")
        settings = self._all_settings.copy()
        temp = settings.copy()
        for key in keys[:-1]:
            settings = settings.setdefault(key, {})
        if action in (self._ACCESS_ACTION_UPDATE, self._ACCESS_ACTION_ADD):
            settings[keys[-1]] = value
            temp[keys[0]].update(settings)
            settings = temp
        elif action == self._ACCESS_ACTION_REMOVE:
            if keys[-1] in settings:
                settings.pop(keys[-1])
                temp[keys[0]].update(settings)
                settings = temp
        elif action == self._ACCESS_ACTION_READ:
            return settings[keys[-1]]
        return settings

    def __getitem__(self, setting):
        return self._access_setting(setting)

    def __setitem__(self, setting, value):
        self._all_settings = self._access_setting(setting, value, self._ACCESS_ACTION_UPDATE)

    def get(self, setting):
        """Returns the specified setting value"""
        return self._access_setting(setting)

    def set(self, setting, value):
        """Adds or updates the specified setting"""
        self._all_settings = self._access_setting(setting, value, self._ACCESS_ACTION_UPDATE)

    def update(self, setting, value):
        """Updates the attribute 'all_settings'. Changes the value of the setting.
        If the setting doesn't exist, it raises a SettingNotFoundError exception."""
        if setting not in self.all_settings.keys():
            raise SettingNotFoundError(f"The setting '{setting}' is not a setting.")
        self._all_settings = self._access_setting(setting, value, self._ACCESS_ACTION_UPDATE)

    def save(self, path):
        """Save to the settings file all new settings"""
        if self.settings_file_type == self.SETTINGS_FILE_TYPE_TOML:
            self._write_toml(path)
        elif self.settings_file_type == self.SETTINGS_FILE_TYPE_JSON:
            self._write_json(path)

    def _write_json(self, path):
        with open(path, "w") as f:
            json.dump(self._all_settings, f, indent=4)

    def _write_toml(self, path):
        with open(path, "w", encoding="utf-8") as f:
            toml.dump(self._all_settings, f)

    def delete(self, setting):
        """
        Removes the configuration specified from the settings dictionary
        :param setting: Specific setting name / key
        """
        self._all_settings = self._access_setting(setting, action=self._ACCESS_ACTION_REMOVE)
        print(self._all_settings)
