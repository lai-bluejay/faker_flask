#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lvl_upgrade_service.db_connections was created on 02/05/2017.
Author: Charles_Lai
Email: laihongchang@   
"""
from sqlalchemy.pool import QueuePool
import records
from faker.config import rootdb_config, server_logger
from mysql_helper import MysqlHelper
# mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]


def sql_connection_by_records(mysql_config):
    """
    返回records的Database对象。 支持with语法。
    :param mysql_config:
    :return:
    """
    DB_URL = 'mysql+pymysql://{user}:{password}@{host}/{database}?autocommit=True'.format(host=mysql_config.host,
                                                                          database=mysql_config.db_name,
                                                                          user=mysql_config.user,
                                                                          password=mysql_config.passwd)
    # 增加预ping，做悲观连接检测，失效则收回连接
    # 增加连接池回收时间，原来为-1，
    # 预设连接池为QueuePool，也可以只通过设定poolsize的方式指定
    # 连接池的最大并发 = pool_size + max_overflow
    # 单连接查询60s超时丢弃
    return records.Database(DB_URL, poolclass=QueuePool, pool_size=30,
                            max_overflow=300, pool_timeout=30, pool_recycle=1200)

try:
    root_db = sql_connection_by_records(rootdb_config)
    root_object = MysqlHelper(root_db)
except Exception as e:
    root_object = None
    server_logger.error(e)
"""
sql = "select * from nvwa"
rows = root_object.query(sql)
print rows[0]
>>> 第一行 <Record {"user": "model", "name": "Hehe"}>
for r in rows:
    print r.user, r.name
    print r[0], r[1]
    print r['user'], r['name']
# to df
user_df = rows.export('df')
# 也可以直接输出到文件

"""
