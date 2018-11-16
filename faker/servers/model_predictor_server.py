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
STOPWORD_PATH = DATA_DIR + "stopwords_cn.txt"
MODEL_PATH = DATA_DIR + "model/"

from faker.models.mode_predictor import Predictor


class ModelPredictorServer(BaseServer):
    def __init__(self, logger_conf=None, logger_handler=None, debug=False):
        super(ModelPredictorServer, self).__init__(
            logger_conf=logger_conf, logger_handler=logger_handler, debug=debug)

    def init(self):
        self.log_list = []
        self.predictor = Predictor(
            stopword_path=STOPWORD_PATH, model_save_path=MODEL_PATH)

    def wizard_server_add_log_list(self):
        log = self.log_list
        return log

    @log_post_parameter(logger=server_logger)
    def predict_string_class(self, **kwargs):
        text = kwargs.get(
            "text", u"python 一个文件运行的时候，会启动一个解析器。这个时候会有一片内存，之后按顺序执行文件")
        ret = self.predictor.prediction(text)
        return ret


model_predictor_server = ModelPredictorServer(logger_handler=server_logger)
app = model_predictor_server.app
