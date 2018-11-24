# -*- coding: utf-8 -*-

from datetime import datetime
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ip = ''
        self.__time_now = datetime.now()

    def prepare(self):
        self.__ip = self.request.headers.get('ip', '')

    def on_finish(self):
        pass

    @property
    def headers(self):
        return {
            'ip': self.__ip,
            'time_now': self.__time_now
        }

    def _output_headers(self):
        self.set_header('ip', self.__ip)
        self.set_header('date', self.__time_now)

    def render_data(self, code, data, msg='success'):
        self._output_headers()
        self.write({'code': code, 'msg': msg, 'data': data})
