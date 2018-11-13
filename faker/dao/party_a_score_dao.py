# -*- coding: utf-8 -*-

import json
import datetime
from faker.config import server_logger
from faker.dbhelper import root_object, medusa_object, hydra_object
import numpy as np


class PartyAScoreDAO(object):
    def __init__(self):
        self.root_db = root_object
        
    def get_score_by_phone(self, phone_list):
        
        return self.root_db.query(
            """
            SELECT
                phone,
                score
            FROM
                nvwa_party_a_score
            WHERE
                phone in ({})
            ORDER BY
                score;
            """.format(','.join(list(map(lambda x: repr(str(x)), phone_list))))
        ).export('df')