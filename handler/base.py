# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from flask_principal import Permission, RoleNeed

invalid_obj = object()
admin_permission = Permission(RoleNeed('admin'))


class BaseHandler(Resource):

    def get_argument(self, arg, default=invalid_obj, required=True, type_=None):
        args = dict()
        args.update(request.args.to_dict())
        args.update(request.form.to_dict())
        args.update(request.json or {})
        data = args.get(arg, default)
        if required and data is invalid_obj:
            raise ValueError('MissingArgument {}'.format(arg))
        if type_:
            data = type_(data)
        return data

    @staticmethod
    def render_data(data=None, *, code='0', msg='ok', chuck=None):
        if chuck and isinstance(chuck, dict) and {'code', 'msg', 'data'}.issubset(chuck):
            return chuck
        else:
            return dict(code=code, msg=msg, data=data)
