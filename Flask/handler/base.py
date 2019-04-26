# -*- coding: utf-8 -*-

from flask_restful import Resource


class BaseHandler(Resource):

    def __init__(self):
        pass

    @staticmethod
    def render_data(data=None, *, code='0', msg='ok', chuck=None):
        if chuck and isinstance(chuck, dict) and {'code', 'msg', 'data'}.issubset(chuck):
            return chuck
        else:
            return dict(code=code, msg=msg, data=data)
