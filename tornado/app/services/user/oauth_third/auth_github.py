# -*- coding: utf-8 -*-

import json
import random
import urllib.parse
import urllib.request
from .auth_base import OAuthBase


class OAuthGITHUB(OAuthBase):
    """
    github不需要获取openid，因此不需要get_open_id()方法
    开发者文档：
    https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = ''
        self.openid = ''

    async def get_auth_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_url,
            'scope': 'user:email',
            'state': str(random.randrange(10 ** 6, 10 ** 7))
        }
        return 'https://github.com/login/oauth/authorize?%s' % urllib.parse.urlencode(params)

    async def get_access_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_key,
            'code': str(code),
            'redirect_url': self.redirect_url,
            'state': str(random.randrange(10 ** 6, 10 ** 7))
        }
        # response = self._post('https://github.com/login/oauth/access_token', params)
        response = await self.post(
            domain='https://github.com',
            path='login/oauth/access_token',
            body=params)
        result = urllib.parse.parse_qs(response, True)
        self.access_token = result['access_token'][0]
        return self.access_token

    async def get_user_info(self):
        params = {'access_token': self.access_token}
        response = self._get('https://api.github.com/user', params)
        # response = await self.get(
        #     domain='https://api.github.com',
        #     path='/user',
        #     query=params)
        result = json.loads(response.decode('utf-8'))
        self.openid = result.get('id', '')
        return result

    async def get_email(self):
        params = {'access_token': self.access_token}
        # response = self._get('https://api.github.com/user/emails', params)
        response = await self.get(
            domain='https://api.github.com',
            path='/user/emails',
            query=params)
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']
