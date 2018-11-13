#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
acm_faker.api_cfg was created on 2018/9/11.
Author: Charles_Lai
Email: laihongchang   
Email: lai.bluejay@gmail.com
"""

from configurations import my_config


class ApiConfig(object):
    def __init__(self):
        pass

    def get_configurations(self, config_name):
        return my_config.get('api', config_name)
