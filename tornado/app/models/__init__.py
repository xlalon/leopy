# -*- coding: utf-8 -*-

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config


class DBServer:
    def __init__(self):
        self.config = Config
        self._instance = {}

    def mysql_db(self):
        if not self._instance.get('mysql_db'):
            engine = create_engine("mysql+pymysql://{user}:{password}@{host}:{port}/{db}".format(
                user=self.config.MySQL_USER,
                password=self.config.MySQL_AUTH,
                host=self.config.MySQL_HOST,
                port=self.config.MySQL_PORT,
                db=self.config.MySQL_DB), max_overflow=5)
            self._instance['mysql_db'] = sessionmaker(bind=engine)()
        return self._instance['mysql_db']

    def redis_db(self):
        if not self._instance['redis_db']:
            self._instance['redis_db'] = redis.Redis(host=self.config.Redis_HOST, password=self.config.Redis_AUTH)
        return self._instance['redis_db']


Base = declarative_base()
