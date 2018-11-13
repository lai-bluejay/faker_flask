#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
/Users/charleslai/PycharmProjects/faker_flask/faker/utils.basic_log.py was created on 2018/11/13.
Author: Charles_Lai
Email: lai.bluejay@gmail.com
"""

from logging import Filter, INFO, WARN, DEBUG, CRITICAL, ERROR
from logging.handlers import TimedRotatingFileHandler
import os
import time
import copy
LOG_DIR = './'
LOG_FILE = 'log'

class MultiProcessTimedRotatingFileHandler(TimedRotatingFileHandler):

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        #if os.path.exists(dfn):
        #    os.remove(dfn)
        if not os.path.exists(dfn):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            # find the oldest log file and delete it
            #s = glob.glob(self.baseFilename + ".20*")
            #if len(s) > self.backupCount:
            #    s.sort()
            #    os.remove(s[0])
            for s in self.getFilesToDelete():
                os.remove(s)
        #print "%s -> %s" % (self.baseFilename, dfn)
        self.mode = 'a'
        self.stream = self._open()
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstNow = time.localtime(currentTime)[-1]
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    newRolloverAt = newRolloverAt - 3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    newRolloverAt = newRolloverAt + 3600
        self.rolloverAt = newRolloverAt

class InfoFilter(Filter):
    def filter(self, record):
        return record.levelno == INFO

class DebugFilter(Filter):
    def filter(self, record):
        return record.levelno == DEBUG

class WarnFilter(Filter):
    def filter(self, record):
        return record.levelno == WARN

class CriticalFilter(Filter):
    def filter(self, record):
        return record.levelno == CRITICAL

class ErrorFilter(Filter):
    def filter(self, record):
        return record.levelno == ERROR

_LOG_SETTING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s\t%(module)s\t%(process)d\t%(message)s'
        },
        'flume': {
            'format': 'log_time=%(asctime)s\tmodule=%(module)s\tprocess=%(process)d\thost=%(host)s\t%(message)s'
        },
    },
    'filters':{
        'DebugFilter':{
            '()': DebugFilter
        },
        'InfoFilter':{
            '()': InfoFilter
        },
        'ErrorFilter':{
            '()': ErrorFilter
        },
        'WarnFilter':{
            '()': WarnFilter
        }
    },
    'handlers': {
        'info_handler': {
            'level': 'INFO',
            #'class': 'logging.handlers.TimedRotatingFileHandler',
            'class': 'faker.utils.basic_log.MultiProcessTimedRotatingFileHandler',
            'filename': LOG_DIR + '/' + LOG_FILE +'.info',
            'backupCount': 14,
            'when':'midnight',
            'formatter': 'flume',
            'filters': ['InfoFilter'],
        },
        'debug_handler': {
            'level': 'DEBUG',
            #'class': 'logging.handlers.TimedRotatingFileHandler',
            'class': 'faker.utils.basic_log.MultiProcessTimedRotatingFileHandler',
            'filename': LOG_DIR + '/' + LOG_FILE + '.debug',
            'backupCount': 14,
            'when':'midnight',
            'formatter': 'standard',
            'filters': ['DebugFilter'],
        },
        'error_handler': {
            'level': 'ERROR',
            #'class': 'logging.handlers.TimedRotatingFileHandler',
            'class': 'faker.utils.basic_log.MultiProcessTimedRotatingFileHandler',
            'filename': LOG_DIR + '/' + LOG_FILE + '.error',
            'backupCount': 14,
            'when':'midnight',
            'formatter': 'standard',
            'filters': ['ErrorFilter'],
        },
        'warn_handler': {
            'level': 'WARN',
            #'class': 'logging.handlers.TimedRotatingFileHandler',
            'class': 'faker.utils.basic_log.MultiProcessTimedRotatingFileHandler',
            'filename': LOG_DIR + '/' + LOG_FILE + '.warn',
            'backupCount': 14,
            'when':'midnight',
            'formatter': 'standard',
            'filters': ['WarnFilter'],
        }
    },
    'loggers': {
        'lhc':{
            'handlers': ['warn_handler','error_handler','debug_handler','info_handler'],
            'propagate': False,
        }

    }
}



def get_basic_log_settings():
    return copy.deepcopy(_LOG_SETTING)
