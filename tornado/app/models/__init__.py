# -*- coding: utf-8 -*-

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config import Config

engine = create_engine("mysql+pymysql://{user}:{password}@{host}:{port}/{db}".format(
                user=Config.MySQL_USER,
                password=Config.MySQL_AUTH,
                host=Config.MySQL_HOST,
                port=Config.MySQL_PORT,
                db=Config.MySQL_DB), max_overflow=5)

mysql_db = scoped_session(sessionmaker(bind=engine, autocommit=True))
redis_db = redis.Redis(host=Config.Redis_HOST, password=Config.Redis_AUTH)
Base = declarative_base()
