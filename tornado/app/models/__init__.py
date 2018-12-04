# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config


class DBServer:
    def __init__(self):
        self.config = Config

    def mysql_db(self):
        engine = create_engine("mysql+pymysql://{user}:{password}@{host}:{port}/{db}".format(
            user=self.config.MySQL_USER,
            password=self.config.MySQL_AUTH,
            host=self.config.MySQL_HOST,
            port=self.config.MySQL_PORT,
            db=self.config.MySQL_DB), max_overflow=5)
        return sessionmaker(bind=engine)()

    def redis_db(self):
        pass


Base = declarative_base()
