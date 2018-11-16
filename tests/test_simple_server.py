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
import pytest
from faker.servers.simple_server import simple_server

# @pytest.fixture
# def test_client():
#     simple_server.app.config['FAKER_ENV'] = 'debug'
#     client = simple_server.app.test_client()
#     yield client


def test_full(client):
    payload = {
        'text': 'hehe',
    }
    td_adaptor_dict = {
        'remote_function': 'simple_rf',
        'args': json.dumps(payload)
    }
    headers = {'content-type': 'application/json'}
    td_srv_ret = client.post('/SimpleServer/', data=json.dumps(td_adaptor_dict), headers=headers, timeout=3)
    ret_body = td_srv_ret
    rd = json.loads(td_srv_ret.content)['result_dict']
    print rd

if __name__ == "__main__":
    import json
    app = simple_server.app
    payload = dict()
    td_adaptor_dict = {
            'remote_function': 'simple_rf',
            'args': json.dumps(payload)
        }
    with app.test_client() as c:
        rv = c.post('/SimpleServer/', data=json.dumps(td_adaptor_dict))
        js_data = json.loads(rv.data)
        assert js_data['code'] == 0