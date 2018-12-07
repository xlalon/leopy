# -*- coding: utf-8 -*-

from datetime import datetime
from tornado.web import RequestHandler
from app.models import DBServer


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ip = ''
        self.__time_now = datetime.now()
        self.__mysql_session = None
        self.__redis_session = None

    @property
    def mysql_db(self):
        self.__mysql_session = DBServer().mysql_db()
        return self.__mysql_session

    @property
    def redis_db(self):
        self.__redis_session = DBServer().redis_db()
        return self.__redis_session

    def prepare(self):
        self.__ip = self.request.headers.get('ip', '')

    def on_finish(self):
        if self.__mysql_session:
            self.__mysql_session.remove()

    @property
    def headers(self):
        return {
            'ip': self.__ip,
        }

    def _output_headers(self):
        self.set_header('ip', self.__ip)

    def get_current_user(self):
        return {'username': 'Leo', 'sex': 'man'}

    def render_data(self, data, code='0', msg='success'):
        self._output_headers()
        self.write({'code': code, 'msg': msg, 'data': data})
