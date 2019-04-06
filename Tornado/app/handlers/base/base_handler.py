# -*- coding: utf-8 -*-

from app.utils.helpers import ObjectDict
from datetime import datetime
from tornado.web import RequestHandler
from app.models import mysql_db, redis_db
from config import Config

_ARG_DEFAULT = object()


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

    def get_req_args(self, *args, args_alias=None, func=None, default=_ARG_DEFAULT):
        """批量获取前端请求参数, 返回一个可根据属性编列的参数字典
        :param args       参数名
        :param args_alias 参数名称更换， 一一对应|特定更换名字
        :param func       self.get_argument
        :param default    若不提供参数默认值，那么缺少参数将会引发异常(对self.get_arguments等无效)
        usage:
        /test?a=10&b=20
        >>> self.get_req_args('a', 'b', 'c', default='')
            {'a': '10', 'b': '20', 'c': ''}
        >>> self.get_req_args('a', 'b', args_alias=['A', 'B'])
            {'A': '10', 'B': '20'}
        >>> self.get_req_args(['a','c'], args_alias={'a': 'A'}, default='1000')
            {'A': '10', 'c': '1000'}
        """
        # 辅助函数
        def is_iter(data):
            return isinstance(data, (list, tuple))
        # 不自定义函数，取self.get_argument，大多数不用自己定义
        func = func or self.get_argument
        # 不定义default当无入参时引发缺少参数异常
        if default is _ARG_DEFAULT:
            default = self._ARG_DEFAULT
        # 提供单个入参或者入参列表/元组支持
        if args and is_iter(args[0]):
            args = list(args[0])
        # 获取参数
        args_dict = dict((arg, func(arg, default=default)) for arg in args)
        # 构造对应别名
        if args_alias is not None:
            if is_iter(args_alias):
                # 如果是列表/元组, 则一一对应
                args_dict = dict((k[1], args_dict[k[0]]) for k in zip(args, args_alias))
            elif isinstance(args_alias, dict):
                # 如果是字典， 则入参名为KEY， 新名字为VALUE
                for old_k, new_k in args_alias.items():
                    args_dict[new_k] = args_dict.pop(old_k, None)
        return ObjectDict(args_dict)

    def render_data(self, data=None, code='0', msg='success', chuck=None):
        self._output_headers()
        if isinstance(chuck, dict) and all((key in chuck.keys()) for key in ('code', 'msg', 'info')):
            self.write(chuck)
        else:
            self.write({'code': code, 'msg': msg, 'data': data})
