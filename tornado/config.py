# -*- coding: utf-8 -*-


class _CodeConfig:
    CODE_OK = '0'
    # 固定8位，前4位为常规的百位， 后4位为个位和十位
    # 比如`404` 为 0100（4）0100（04）
    CODE_PAGE_NOT_FOUND = '01000100'
    CODE_GITHUB_OAUTH_FAIL = '01000001'
    CODE_ACCOUNT_EXIST = '01000011'
    CODE_ACCOUNT_WRONG = '01000001'


class _MSGConfig:
    MSG_OK = 'success'
    MSG_PAGE_NOT_FOUND = 'error! page not found.'
    MSG_ACCOUNT_EXIST = 'The email or nickname has been registered, please change another!'
    MSG_ACCOUNT_WRONG = 'Your email or password not right, please login again!'


class _DBConfig:
    MySQL_HOST = '127.0.0.1'
    MySQL_PORT = '3306'
    MySQL_USER = 'root'
    MySQL_AUTH = 'Xiao0000'
    MySQL_DB = 'leopy'
    Redis_HOST = '127.0.0.1'
    Redis_PORT = 6379
    Redis_USER = ''
    Redis_AUTH = ''
    Redis_DB = '0'


class _OauthConfig:
    GITHUB_ID = '34a4a42c445859c6becf'
    GITHUB_KEY = 'db5c02e0ccd75284d69605345710e6eab5ae372a'
    GITHUB_CALLBACK_URL = 'http://127.0.0.1:1024/user/oauth/github_check'


class Config(_CodeConfig, _MSGConfig, _DBConfig, _OauthConfig):
    secret_key = "leo's secret key, no one can guess it!"
    domain = 'http://api.shetest18.cn'
    pass
