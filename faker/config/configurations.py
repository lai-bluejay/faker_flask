#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lvl_upgrade_service.configurations was created on 03/05/2017.
Author: Charles_Lai
Email: laihongchang@   
Email: lai.bluejay@gmail.com
"""

import ConfigParser
import os

from faker.utils.log_utils import init_log_from_config, logger as ori_logger

root = os.path.dirname(__file__)

import copy
import logging
import logging.config
import socket
import getpass

# QA
import sys
sys.path.append('.')
from faker.utils import env

MACHINE_NAME = socket.getfqdn(socket.gethostname())
USER_NAME = getpass.getuser()

BASE = "Base"
LOG_DIR = "log_dir"
LOG_FILE = "log_file"
LOG_LEVEL = "log_level"

class MyConfig(object):
    def __init__(self, method):
        """
        输入 test 或者是 real
        :param method:
        :return:
        """
        self.method = method
        if method != 'test' and method != "production" and method != "local":
            exit("please init config with test or real")
        config = ConfigParser.ConfigParser()
        config.readfp(open("{0}/../conf/{1}/db.conf".format(root, method)))
        self.config = config
        self.init_log_handle()

    def get(self, key, field):
        return self.config.get(key, field)

    def init_log_handle(self, base=BASE):
        """
        变成全局可用的公共logger_handle
        其中，logger.info(), 保证一次请求只有一条记录。内容格式为k_1=v_1\tk_2=v_2。 目的方便收集日志信息。
        logger.debug()/warn(), 可以每次需要都打印.
        logger.error(),  在重点抛出异常的地方进行记录
        :return:
        """
        log_fpath = os.path.join(root, '../conf/{0}/log.conf'.format(self.method))
        parser = ConfigParser.ConfigParser()
        parser.read(log_fpath)
        required_ops = [(base, LOG_DIR), (base, LOG_FILE), (base, LOG_LEVEL)]
        for sec, op in required_ops:
            if not parser.has_option(sec, op):
                raise Exception("Log load config file failed")
        log_dir = parser.get(base, LOG_DIR)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        try:
            logger = init_log_from_config(log_fpath, base=base)
        except:
            logger = ori_logger
        return logger

if env.DEBUG:
    config_type = "test"
else:
    config_type = "local"
my_config = MyConfig(config_type)
server_logger = my_config.init_log_handle(BASE)
if config_type == 'local':
    # server_logger.info('hehehe, config done')
    server_logger.debug('hehehe, config done')

CFG_FILE = os.path.join(root, '../conf/{0}/cfg.conf'.format(config_type))
MNS_CFG = os.path.join(root, '../conf/{0}/sample.cfg'.format(config_type))
