# -*- coding:utf-8 -*-
from configurations import my_config


class MysqlConfig:
    def __init__(self, config_name):
        self.__get_configurations(config_name)

    def __get_configurations(self, config_name):
        self.host = my_config.get(config_name, 'MYSQL_HOST')
        self.user = my_config.get(config_name, 'MYSQL_USER')
        self.passwd = my_config.get(config_name, 'MYSQL_PW')
        self.db_name = my_config.get(config_name, 'MYSQL_DATABASE')
