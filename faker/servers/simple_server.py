#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
/Users/charleslai/PycharmProjects/faker_flask/faker/servers.model_predictor_server.py was created on 2018/11/13.
file in :relativeFile
Author: Charles_Lai
Email: lai.bluejay@gmail.com
"""
import os
import sys
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append("%s/../.." % root)
sys.path.append("%s/.." % root)
sys.path.append(u"{0:s}".format(root))
from faker.servers.base_server import BaseServer
from faker.config import server_logger
from faker.utils.log_utils import log_post_parameter
from faker.utils import DATA_DIR


class SimpleServer(BaseServer):
    def __init__(self, logger_conf=None, logger_handler=None, debug=False):
        super(SimpleServer, self).__init__(
            logger_conf=logger_conf, logger_handler=logger_handler, debug=debug)

    def init(self):
        self.log_list = []

    def wizard_server_add_log_list(self):
        log = self.log_list
        return log

    @log_post_parameter(logger=server_logger)
    def simple_rf(self, **kwargs):
        text = 'Hello World'
        return text


simple_server = SimpleServer(logger_handler=server_logger)
app = simple_server.app
