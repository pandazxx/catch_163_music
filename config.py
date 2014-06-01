__author__ = 'pandazxx'


_DEFAULT_CONFIG = {
    "file_path_pattern": "{song.album.artist_description}/{song.album.name}/{song.name}",
    "download_dir": "./",
}


import yaml
import os.path


class Config(object):
    def __init__(self):
        self.__config_dict = _DEFAULT_CONFIG.copy()

    def load_config_from_file(self, file_path):
        user_config = {}
        with open(file_path, 'r') as file:
            user_config = yaml.load(file.read())
            print(user_config)
            self.__config_dict.update(user_config)

    def get(self, key):
        return self.__config_dict.get(key)


_global_config = None

def init_config(conf_file_path="~/.music163.conf"):
    global _global_config
    if not _global_config:
        _global_config = Config()
        conf_file_path = os.path.abspath(os.path.expanduser(conf_file_path))
        print(conf_file_path)
        if os.path.exists(conf_file_path):
            print("exist")
            _global_config.load_config_from_file(conf_file_path)

def get_config():
    return _global_config
