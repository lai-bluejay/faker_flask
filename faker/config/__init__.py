# -*- coding: utf-8 -*-
"""
lvl_upgrade_service.__init__.py was created on 12/04/2017.
Author: Charles_Lai
Email: laihongchang@   
Email: lai.bluejay@gmail.com
"""

from configurations import my_config, server_logger
from mysql import MysqlConfig
from mongo import MongoConfig
from api_cfg import ApiConfig
from configurations import config_type
# mysql_config, 直接取section的名字即可
rootdb_config = MysqlConfig('root')
# API
api_cfg_object = ApiConfig()

hehe_api = api_cfg_object.get_configurations('hehe_api')
