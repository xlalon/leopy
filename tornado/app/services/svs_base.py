# -*- coding: utf-8 -*-

import urllib.parse
import urllib.request


class BaseService:

    def __init__(self, *args, **kwargs):
        pass

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
