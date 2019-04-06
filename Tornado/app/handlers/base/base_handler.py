# -*- coding: utf-8 -*-

from app.utils.helpers import ObjectDict
from datetime import datetime
from tornado.web import RequestHandler, MissingArgumentError
from app.models import mysql_db, redis_db
from config import Config

_INVALID_VALUE = object()


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ip = None
        self.__time_now = datetime.now()
        self.__mysql_session = None
        self.__redis_session = None
        self.__SiteUID = None
        self.__Token = None
        self.config = Config

    @property
    def mysql_db(self):
        self.__mysql_session = mysql_db
        return self.__mysql_session

    @property
    def redis_db(self):
        self.__redis_session = redis_db
        return self.__redis_session

    def prepare(self):
        self.__ip = self.request.headers.get('Ip', '')
        self.__SiteUID = self.request.headers.get('SiteUID', 'iosshus')
        self.__Token = self.request.headers.get('Token', '')

    def on_finish(self):
        if self.__mysql_session:
            self.__mysql_session.remove()

    @property
    def headers(self):
        return {
            'Ip': self.__ip,
            'SiteUID': self.__SiteUID,
            'Token': self.__Token
        }

    def _output_headers(self):
        self.set_header('Ip', self.__ip)
        self.set_header('SiteUID', self.__SiteUID)
        self.set_header('Token', self.__Token)

    def get_current_user(self):
        return {'username': 'Leo', 'sex': 'man'}

    def get_params(self, *args, dft=None, result_type=None):
        """批量获取前端请求参数, 返回一个可根据属性编列的参数字典
         usage:a=1&b=2
         get_params('a', 'b', 'c')   -> {'a': '1', 'b': '2', 'c': None}
         get_params(['a', 'b', 'c']) -> {'a': '1', 'b': '2', 'c': None}
         get_params('a', 'b', 'c', dft='DEFAULT', result_type=list) > ['1', '2', 'DEFAULT']
        """
        return self._get_params(*args, dft=dft, result_type=result_type)

    def _get_params(self, *args, dft=None, result_type=None):
        if len(args) < 1:
            raise ValueError('get_params empty args')
        args_ = None
        if len(args) == 1:
            args = args[0]
            if isinstance(args, str):
                return self.get_argument(args, dft)
            elif isinstance(args, (list, tuple)):
                args_ = args
        else:
            args_ = args
        result = map(self.get_argument, args_, [dft]*len(args_))
        if result_type in (None, dict):
            return ObjectDict(dict(zip(args_, result)))
        elif result_type in (list, tuple):
            return result_type(result)
        else:
            return None

    def render_data(self, data=None, code='0', msg='success', chuck=None):
        self._output_headers()
        if isinstance(chuck, dict) and all((key in chuck.keys()) for key in ('code', 'msg', 'info')):
            self.write(chuck)
        else:
            self.write({'code': code, 'msg': msg, 'data': data})
