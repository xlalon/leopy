#! /usr/bin/env python

from models import db


class BaseService:
    def __init__(self):
        self.db = db
        self.ResponseStatus = ResponseStatus
        self.ResponseMessages = ResponseMessages


class ResponseStatus:
    CODE_OK = 200
    CODE_USER_NOT_EXISTS = 404001
    CODE_USER_STATUS_INACTIVE = 404002

    CODE_USER_PASSWORD_MISMATCH = 401001
    CODE_USER_EXISTS = 403002


class ResponseMessages:
    MSG_OK = 'ok'
    MSG_USER_NOT_EXISTS = 'user not exists'
    MSG_USER_STATUS_INACTIVE = 'user status not active'
    MSG_USER_PASSWORD_MISMATCH = 'password wrong'
    MSG_USER_EXISTS = 'email had been registered.'

