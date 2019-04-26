# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def _env_config():
    config_parser = ConfigParser()
    config_parser.read(os.path.join(BASE_DIR, '.env'))
    return config_parser['conf']


ENV_CONFIG = _env_config()


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{passoword}@{host}:{port}/{database}?charset=utf8mb4'.format(
        username=ENV_CONFIG['MYSQL_USERNAME'],
        passoword=ENV_CONFIG['MYSQL_PASSWORD'],
        host=ENV_CONFIG['MYSQL_HOST'],
        port=ENV_CONFIG['MYSQL_PORT'],
        database=ENV_CONFIG['MYSQL_DATABASE']
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = int(ENV_CONFIG['POOL_SIZE'])
    SQLALCHEMY_POOL_TIMEOUT = int(ENV_CONFIG['POOL_TIMEOUT'])
    SQLALCHEMY_POOL_RECYCLE = int(ENV_CONFIG['POOL_RECYCLE'])
