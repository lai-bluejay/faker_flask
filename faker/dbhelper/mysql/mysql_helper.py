#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
acm_faker.mysql_helper was created on 2018/8/15.
Author: Charles_Lai
Email: laihongchang@   
Email: lai.bluejay@gmail.com
"""
from faker.config import server_logger
from faker.utils.nvwa_utils import retry
from sqlalchemy.exc import OperationalError


class MysqlHelper(object):
    def __init__(self, db):
        """

        :param db: records.Database 对象
        """
        self._db = db
        assert self._db is not None

    @retry(attempt=5, timeout=1)
    def query(self, sql, fetchall=False, **kwargs):
        """
        执行 select 操作
        :param sql:
        :param fetchall: If True, no lazy query, else lazy query.
        :param kwargs:
        :return:
        """

        try:
            result = self._db.query(sql, fetchall=fetchall, *kwargs)
        except OperationalError as e:
            server_logger.error(e)
            server_logger.error(sql)
            self._db._engine.pool.dispose()
            server_logger.error("Dispose connections that are idle in the pool, return new Pool.")
            result = self._db.query(sql, fetchall=fetchall, *kwargs)
        except Exception as e:
            server_logger.error(e)
            server_logger.error(sql)
            self._db.db = self._db._engine.connect()
            result = self._db.query(sql, fetchall=fetchall, *kwargs)
        return result

    def dispose(self):
        """
        dispose idle connection, and NEW Pool().
        :return:
        """
        self._db._engine.pool.dispose()

    def close(self):
        return self._db.close()
