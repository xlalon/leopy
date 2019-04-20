# -*- coding: utf-8 -*-

from app.business.user.oauth_github import GithubCheckBus
from config import Config
from app.handler.base.base_handler import BaseHandler
from app.service.user.oauth_third.auth_github import OAuthGITHUB


class GithubOauthHandler(BaseHandler):

    async def post(self):
        """获取github认证路由"""
        data = {
            'url': await OAuthGITHUB(
                Config.GITHUB_ID,
                Config.GITHUB_KEY,
                Config.GITHUB_CALLBACK_URL).get_auth_url()
        }
        return self.render_data(data=data)

    async def get(self):
        request_code = self.request.query_arguments.get('code')[0].decode('utf-8')
        code, msg, data = await GithubCheckBus().github_check(request_code=request_code)
        return self.render_data(code=code, msg=msg, data=data)
