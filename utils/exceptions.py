# -*- coding: utf-8 -*-

from flask import jsonify


class MyException(RuntimeError):
    status_code = 200

    def __init__(self, msg=None, data=None, code=None):
        self.msg = msg
        self.data = data
        self.code = code

    def to_json(self, msg=None, data=None, code=None):
        if not code:
            code = self.status_code
        return jsonify({'code': code, 'msg': msg, 'data': data})


class PermissionDenied(MyException):
    status_code = 403

