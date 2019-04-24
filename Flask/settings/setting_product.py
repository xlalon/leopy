# -*- coding: utf-8 -*-


from .setting import Config


class ProductConfig(Config):
    ENV = 'production'
    DEBUG = False
    SECRET_KEY = b'\x17=L\x16\xe6*\x91\x136X\x1d*I\xd10s}\xff5\xb3\x8c)\xdd\x82q\xf0\xb5\xb8\xa3\x80\xc9N'
