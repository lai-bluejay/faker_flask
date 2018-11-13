#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
faker.log_utils was created on 2018/7/19.
Author: Charles_Lai
Email: lai.bluejay@gmail.com
"""
# QA
import os
import sys
sys.path.append('.')
import time
import logging
import socket
import ConfigParser
from functools import wraps  # use this to preserve function signatures and docstrings
from faker.utils.basic_log import get_basic_log_settings
import copy
from logging import config, LoggerAdapter
import logging.config
import socket
import getpass
from faker.utils import ROOT_DIR

# 记录时间用的装饰器
# --exe_time

def retry(attempt=3, timeout=1):
    # 每次retry sleep不同的间隔，给服务器喘息的机会
    # 第一次 1s，第二次2s，以此类推
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while True:
                try:
                    return func(*args, **kw)
                except Exception as e:
                    if att < attempt:
                        att += timeout
                        time.sleep(att)
                    else:
                        raise

        return wrapper

    return decorator

class LoggerAdapterCustomer(LoggerAdapter):
    """
    An adapter for loggers which makes it easier to specify contextual
    information in logging output.
    cpython haven't warn  
    """
    def __init__(self, logger, extra):
        LoggerAdapter.__init__(self, logger, extra)

    def warn(self, msg, *args, **kwargs):
        """
        Delegate a warning call to the underlying logger, after adding
        contextual information from this adapter instance.
        """
        msg, kwargs = self.process(msg, kwargs)
        self.logger.warning(msg, *args, **kwargs)

def exe_time(logger):
    def out_wrapper(func):
        @wraps(func)
        def newFunc(*args, **args2):
            t0 = time.time()
            back = func(*args, **args2)
            try:
                logger.debug("class_name={}\tfunc_name={}\tcost_time={}".format(args[0].__class__.__name__, func.__name__,
                                                                                round(time.time()-t0, 4)))
            except:
                logger.debug("func_name={}\tcost_time={}".format(
                    func.__name__, round(time.time() - t0, 4)))
            return back
        return newFunc
    return out_wrapper
# --end of exe_time

# test exe decorator


def exe_time_v0(func):
    @wraps(func)
    def newFunc(*args, **args2):
        logger = logging.getLogger(args[0].__class__.__name__)
        t0 = time.time()
        # logger.info( "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        back = func(*args, **args2)
        # logger.info( "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        try:
            logger.debug(
                "class_name={}\tfunc_name={}\tcost_time={}".format(args[0].__class__.__name__, func.__name__,
                                                                   round(time.time() - t0, 4)))
        except:
            logger.debug("func_name={}\tcost_time={}".format(
                func.__name__, round(time.time() - t0, 4)))
        return back
    return newFunc


def log_post_parameter(logger):
    def out_wrapper(func):
        @wraps(func)
        def newFunc(*args, **args2):
            t0 = time.time()
            back = func(*args, **args2)
            try:
                logs = "class_name={}\tfunc_name={}\tcost_time={}\tpost_param={}".format(args[0].__class__.__name__,
                                                                                         func.__name__, round(time.time()-t0, 4), str(args2))
                logger.debug(logs)
            except:
                logs = "func_name={}\tcost_time={}\tpost_param={}".format(
                    func.__name__, round(time.time() - t0, 4), str(args2))
                logger.debug(logs)
            return back
        return newFunc
    return out_wrapper


MACHINE_NAME = socket.getfqdn(socket.gethostname())
USER_NAME = getpass.getuser()

BASE = "Base"
LOG_DIR = "log_dir"
LOG_FILE = "log_file"
LOG_LEVEL = "log_level"


def init_log_from_config(cfg_file, formatter='standard', base=BASE):
    required_ops = [(base, LOG_DIR), (base, LOG_FILE), (base, LOG_LEVEL)]
    parser = ConfigParser.ConfigParser()
    parser.read(cfg_file)
    for sec, op in required_ops:
        if not parser.has_option(sec, op):
            raise Exception("Log load config file failed")
    log_dir = parser.get(base, LOG_DIR)
    log_file = parser.get(base, LOG_FILE)
    # add default hostname suffix for log_file
    log_level = parser.get(base, LOG_LEVEL)
    settings = get_basic_log_settings()
    settings['handlers']['info_handler']['filename'] = log_dir + \
        '/' + log_file + '.info'
    settings['handlers']['debug_handler']['filename'] = log_dir + \
        '/' + log_file + '.debug'
    settings['handlers']['warn_handler']['filename'] = log_dir + \
        '/' + log_file + '.warn'
    settings['handlers']['error_handler']['filename'] = log_dir + \
        '/' + log_file + '.error'
    if formatter == 'flume':
        settings['handlers']['info_handler']['formatter'] = formatter
        settings['handlers']['debug_handler']['formatter'] = formatter
        settings['handlers']['warn_handler']['formatter'] = formatter
        settings['handlers']['error_handler']['formatter'] = formatter
    settings['loggers'][log_file] = copy.deepcopy(settings['loggers']['lhc'])
    logging.config.dictConfig(settings)
    extra_dict = {"host": MACHINE_NAME}
    logger = logging.getLogger(log_file)
    logger.propagate = False
    if log_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif log_level == 'INFO':
        logger.setLevel(logging.INFO)
    elif log_level == 'WARN':
        logger.setLevel(logging.WARN)
    elif log_level == 'ERROR':
        logger.setLevel(logging.ERROR)
    else:
        raise ("unknown log level:[%s]" % log_level)
    return LoggerAdapterCustomer(logger, extra_dict)


logger = init_log_from_config(ROOT_DIR + '/conf/local/log.conf')