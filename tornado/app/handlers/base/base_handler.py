# -*- coding: utf-8 -*-

from datetime import datetime
from tornado.web import RequestHandler
from app.models import DBServer
from config import Config


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
        self.__mysql_session = DBServer().mysql_db()
        return self.__mysql_session

    @property
    def redis_db(self):
        self.__redis_session = DBServer().redis_db()
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

    def render_data(self, data, code='0', msg='success', chuck=None):
        self._output_headers()
        if isinstance(chuck, dict) and all((key in chuck.keys()) for key in ('code', 'msg', 'info')):
            self.write(chuck)
        else:
            self.write({'code': code, 'msg': msg, 'data': data})
