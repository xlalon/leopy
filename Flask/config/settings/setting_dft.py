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
