#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
/Users/charleslai/PycharmProjects/faker_flask/tests.test_model_predict_server.py was created on 2018/11/13.
file in :relativeFile
Author: Charles_Lai
Email: lai.bluejay@gmail.com
"""
import os
import sys
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append("%s/../.." % root)
sys.path.append("%s/.." % root)
sys.path.append("%s/../../.." % root)
sys.path.append(u"{0:s}".format(root))

import json
import requests


def test_full(text):
    payload = {
        'text': text,
    }
    td_adaptor_dict = {
        'remote_function': 'simple_rf',
        'args': json.dumps(payload)
    }
    url = 'http://0.0.0.0:12345/SimpleServer/'
    headers = {'content-type': 'application/json'}
    td_srv_ret = requests.post(url, data=json.dumps(td_adaptor_dict), headers=headers, timeout=3)
    ret_body = td_srv_ret
    rd = json.loads(td_srv_ret.content)['result_dict']
    print rd


if __name__ == "__main__":
    text = 'sys.argv[1]'
    test_full(text)
