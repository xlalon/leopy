# -*- coding: utf-8 -*-


class BaseBusiness:

    def __init__(self, mysql_db=None, redis_db=None):
        self.mysql_db = mysql_db
        self.redis_db = redis_db
