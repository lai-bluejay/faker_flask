# -*- coding:utf-8 -*-
from configurations import my_config

class MongoConfig:
    def __init__(self, config_name):
        self.__get_configurations(config_name)

    def __get_configurations(self, config_name):
        self.host = my_config.get(config_name, 'HOST')
        self.user = my_config.get(config_name, 'MONGO_USER')
        self.passwd = my_config.get(config_name, 'MONGO_PW')
        self.db_name = my_config.get(config_name, 'NAME')
        self.port = int(my_config.get(config_name, 'PORT'))
        self.alias = my_config.get(config_name, 'ALIAS')
