# -*- coding: utf-8 -*-

from .setting_dft import Config


class DevDeConfig(Config):
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Xiao0000@127.0.0.1:3306/leo'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
