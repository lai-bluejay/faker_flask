#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
faker.common_model_dao was created on 2018/7/16.
Author: Charles_Lai
Email: laihongchang@   
Email: lai.bluejay@gmail.com
"""
import json
import datetime
from faker.config import server_logger
from faker.dbhelper import root_object
class CommonModelDao(object):
    def __init__(self):
        self.root_db = root_object

