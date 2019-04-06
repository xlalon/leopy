# -*- coding: utf-8 -*-

import json
import urllib.parse
from app.routers import make_app
from tornado.testing import AsyncHTTPTestCase
from app.utils.helpers import ObjectDict


class BaseTestCase(AsyncHTTPTestCase):
    def setUp(self):
        super().setUp()

    @property
    def headers(self):
        headers = dict(
            SiteUID='app',
            AppVersion='6.4.6',
            LocalCountry='US'
        )
        headers['Token'] = self.token
        return headers

    @property
    def token(self):
        return '4286123051792_5c18a32f947758.70129474_2b6c497b4444792c554fe2c8c713394289929e40'

    @token.setter
    def token(self, token_new):
        self.token = token_new

    # def change_user(self, username, password):
    #     return '4286123051792_5c18a32f947758.70129474_2b6c497b4444792c554fe2c8c713394289929e40'

    def get_app(self):
        return make_app()

    def fetch(self, path, query=None, body=None, **kwargs):
        if query:
            path = '{}?{}'.format(path, urllib.parse.urlencode(query=query))
        if kwargs.get('method', 'GET').upper() == 'POST' and body:
            body = urllib.parse.urlencode(body)
        return super().fetch(path=path, body=body, **kwargs)

    def get(self, path, query=None, **kwargs):
        return self.fetch(path, query=query, method='GET', **kwargs)

    def post(self, path, query=None, body=None, **kwargs):
        return self.fetch(path, query=query, body=body, method='POST', **kwargs)

    @staticmethod
    def res2_data(response):
        """
        :param response: nj接口响应
        :return: 解析成功返回一个可以通过实例属性遍历的字典结构, 解析失败返回None
        """
        from json import JSONDecodeError
        try:
            return ObjectDict(data=json.loads(response.body))
        except JSONDecodeError:
            return None
