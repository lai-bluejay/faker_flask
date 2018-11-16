# -*- encoding: utf-8  -*-
import os
import re
import abc
import sys
reload(sys)	
sys.setdefaultencoding("utf-8")
import time
import json
import base64
import socket
import datetime
import traceback
#import ruamel.yaml as yaml
from flask import Flask, request, g
from gevent.wsgi import WSGIServer
from faker.utils.log_utils import init_log_from_config, logger as ori_logger

RET_ERRNO = 'code'
RET_MSG = 'msg'
RET_DATA = 'result_dict'

# pylint: disable=E0202
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

ERROR_CODE = {
    0 :  u'响应成功',

    401: u'缺少参数',
    404: u'未找到服务',
    402: u'payload反序列化失败',
    403: u'remote_function获取失败',
    405: u'参数json反序列化失败',
    500: u'内部错误',
}

class BaseServer(object):
    __metaclass__ = abc.ABCMeta
    app = Flask(__name__,instance_relative_config=True)

    def __init__(self, logger_conf=None, logger_handler=None, debug=False):
        self._base_server_name = self.__class__.__name__
        self._base_server_path = '/'+str(self._base_server_name)+'/'
        self._base_server_logger_handler = logger_handler
        self._base_server_logger_file = logger_conf
        self._base_server_trace_client = None
        self._base_server_local_ip = socket.gethostbyname(socket.gethostname())
        self.check_params_list = []
        self._base_server_debug = self._env_check() if not debug else True
        self._base_server_init()
        self.init()

    def init(self):
        pass

    def _env_check(self):
        hostname = socket.gethostname()
        if 'anubis' in hostname or 'horus' in hostname:
            return False

    def base_trace_error(self, error_msg=''):
        except_detail = traceback.format_exc()
        self._base_server_trace_error('other:'+error_msg, except_detail)

    def _base_server_trace_error(self, error_msg, error_detail=''):
        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = self._base_server_name+":"+error_msg
        self.logger.error('error_msg[%s] error_detail[%s]' %(error_msg, error_detail))
        if not self._base_server_debug and False:
            error_msg = error_msg.split('user_id')[0].split('order_id')[0].split('###')[0]
            msg = 'log_time=%s\terror_msg=%s\tlocal_ip=%s\tpid=%s' %(log_time, error_msg, self._base_server_local_ip, os.getpid())

    def _collect_errormsg_decorator(self, func):
        def wrapper(*args, **kwargs):
            try:
                return True, func(*args, **kwargs)
            except Exception, e:
                # print traceback.print_exc()
                except_detail = traceback.format_exc()
                self._base_server_trace_error( '%s:%s' %(func.__name__, e.message), except_detail)
                return False, '%s:%s' %(func.__name__, e.message)
        return wrapper

    def _base_server_init_flask(self):
        base_server_init_flask(self.app, log_list=self.base_server_add_log_list,
                check_params_list=self.check_params_list,base_path=self._base_server_path,
                agent_class=self, logger=self.logger, collect_errormsg_decorator=self._collect_errormsg_decorator)

    def _base_server_init(self):
        self._base_server_init_logger()
        self._base_server_init_flask()

    def _base_server_init_logger(self):
        try:
            if self._base_server_logger_handler:
                self.logger = self._base_server_logger_handler
            elif self._base_server_logger_file:
                self.logger = init_log_from_config(self._base_server_logger_file)
            else:
                self.logger = ori_logger
        except:
            print 'custom logger failed, choose default logger'
            print traceback.print_exc()
            self.logger = ori_logger

    def base_server_add_log_list(self):
        log = []
        log.append('order_id=%s' %g.args['order_id'])
        log.append('user_id=%s' %g.args['user_id'])
        return log

    def base_server_run(self, port):
        if self._base_server_debug:
            self.app.run('0.0.0.0',port)
        else:
            http_server = WSGIServer(('',port), self.app)
            http_server.serve_forever()


def base_server_init_flask(app=None, log_list=lambda :[], check_params_list=[], base_path='/base/',
                             agent_class=None, logger=None, collect_errormsg_decorator=None):

    def before_request():
        g.method = request.method
        g.path = request.path
        g.remote_ip = request.headers.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        g.start = time.time()
        g.end = None
        g.at = 0
        g.errno = 0
        g.log = []
        if g.path <> base_path:
            g.errno = 404
            ret_dict = {
                RET_ERRNO: g.errno,
                RET_MSG: ERROR_CODE[g.errno],
                RET_DATA: None
            }
            logger.error('error_msg=%s\trequest_path=%s\tserver_path=%s' %(ERROR_CODE[g.errno], g.path, base_path))
            return json.dumps(ret_dict)

        g.post_dict = request.get_json(force=True, silent=True)
        if g.post_dict is False or g.post_dict is None:
            g.errno = 402
            ret_dict = {
                RET_ERRNO: g.errno,
                RET_MSG: ERROR_CODE[g.errno],
                RET_DATA: None
            }
            logger.error('error_msg=%s\trequest_data=%s' %(ERROR_CODE[g.errno], g.post_dict))
            return json.dumps(ret_dict)

        if not (g.post_dict.has_key('remote_function') and
                hasattr(agent_class, g.post_dict['remote_function'])):
            g.errno = 403
            ret_dict = {
                RET_ERRNO: g.errno,
                RET_MSG: ERROR_CODE[g.errno],
                RET_DATA: None
            }
            logger.error('error_msg=%s\trequest_funciton=%s' %(ERROR_CODE[g.errno], g.post_dict.get('remote_function')))
            return json.dumps(ret_dict)

        g.remote_function = g.post_dict['remote_function']

        def _check_parmas_list():
            g.args = json.loads(g.post_dict.get('args'))
            #g.args = yaml.safe_load(g.post_dict.get('args'))
            for check_ele in check_params_list:
                assert g.args.has_key(check_ele)
            return True

        ret_status,_ = collect_errormsg_decorator(_check_parmas_list)()
        if not ret_status:
            g.errno = 401
            ret_dict = {
                RET_ERRNO: g.errno,
                RET_MSG: ERROR_CODE[g.errno],
                RET_DATA: None
            }
            logger.error('error_msg=%s' %(ERROR_CODE[g.errno]))
            return json.dumps(ret_dict)

    def teardown_request(exc):
        g.end = time.time()
        g.at = g.end - g.start
        if True:
            log = [
                'method=%s' % g.method,
                'path=%s' % g.path,
                'remote_ip=%s' % g.remote_ip,
                'server=%s' % base_path,
                'all_cost=%f' % g.at,
                'error=%d' % g.errno,
                ]
        if hasattr(g, 'remote_function'):
            log.append("remote_function=%s" %g.remote_function)

        if hasattr(g, 'args'):
            ret_status, extend_log = collect_errormsg_decorator(log_list)()
            if ret_status:
                log.extend(extend_log)
        logger.info('\t'.join(log))


    @app.route(base_path, methods=['POST'])
    def _server_run():
        ret_dict = {
                RET_ERRNO: 0,
                RET_MSG: '',
                RET_DATA:{},
            }
        ret_status, content = collect_errormsg_decorator(getattr(agent_class, g.remote_function))(**g.args)

        if ret_status:
            ret_dict[RET_ERRNO] = 0
            ret_dict[RET_DATA] = content
        else:
            ret_dict[RET_ERRNO] = 500
            ret_dict[RET_MSG] = content
        return json.dumps(ret_dict, cls=CJsonEncoder)

    @app.route("/health", methods=['HEAD', 'GET'])
    def _heathy_listen():
        """"用于端口健康监测"""
        
        ret_dict = {
                RET_ERRNO: 0,
                RET_MSG: ERROR_CODE[0],
                RET_DATA:"Healthy port.",
            }
        return json.dumps(ret_dict, cls=CJsonEncoder)

    app.before_request(before_request)
    app.teardown_request(teardown_request)

