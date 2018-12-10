# -*- coding: utf-8 -*-

import json
import urllib.parse
import urllib.request
from json import JSONDecodeError
from tornado.web import HTTPError
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from config import Config


class BaseService:

    def __init__(self, *args, **kwargs):
        self.config = Config

    @staticmethod
    def _get(url, data):
        request_url = '%s?%s' % (url, urllib.parse.urlencode(data))
        response = urllib.request.urlopen(request_url)
        return response.read()

    @staticmethod
    def _post(url, data):
        request = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(encoding='UTF8'))
        response = urllib.request.urlopen(request)
        return response.read()

    async def get(self, domain, path=None, query=None, **kwargs):
        request = self.make_request(domain, path, query, **kwargs)
        try:
            response = await AsyncHTTPClient().fetch(request)
            return self.parse_response(response)
        except HTTPError:
            return None

    async def post(self, domain, path=None, query=None, method='POST', body=None, **kwargs):
        request = self.make_request(domain, path, query, body=body, method=method, **kwargs)
        try:
            response = await AsyncHTTPClient().fetch(request)
            return self.parse_response(response)
        except HTTPError:
            return None

    @staticmethod
    def make_request(domain, path=None, query=None, body=None, headers=None, **kwargs):
        url = urllib.parse.urljoin(domain, path)
        if isinstance(query, dict):
            url = '{}?{}'.format(url, urllib.parse.urlencode(query))
        if isinstance(body, dict):
            body = urllib.parse.urlencode(body).encode(encoding='UTF8')
        return HTTPRequest(url=url, body=body, headers=headers, **kwargs)

    @staticmethod
    def parse_response(response):
        if not response.body:
            return None
        try:
            return json.loads(response.body.decode())
        except JSONDecodeError:
            return response.body.decode()
