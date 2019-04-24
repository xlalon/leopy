# -*- coding: utf-8 -*-


import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    ENV = 'development'
    DEBUG = True
    SECRET_KEY = 'YOU NEVER GUESS THE KEY'


del os
