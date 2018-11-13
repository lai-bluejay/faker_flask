# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from pymongo import MongoClient


def get_mongodb_connection(*args, **kwargs):
    """
    Get MongoDB connection by given parameters.
    :param kwargs
    :return 
    """
    return MongoClient(*args, **kwargs)
