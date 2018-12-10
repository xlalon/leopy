# -*- coding: utf-8 -*-

from tornado.gen import multi
from app.utils.helpers import dict_get
from config import Config
from app.services.user.oauth_third.auth_github import OAuthGITHUB


class GithubCheckBus:

    def __init__(self):
        self.oauth_svs = OAuthGITHUB(Config.GITHUB_ID, Config.GITHUB_KEY, Config.GITHUB_CALLBACK_URL)

    async def github_check(self, request_code):
        await self.oauth_svs.get_access_token(request_code)
        try:
            github_data = await multi({
                # 'access_token': self.oauth_svs.get_access_token(request_code),
                # 'user_info': self.oauth_svs.get_user_info(),
                'user_email': self.oauth_svs.get_email()
            })
        except Exception as e:
            print(e)

            # 获取令牌/用户信息失败，反馈失败信息
            code = Config.CODE_GITHUB_OAUTH_FAIL
            msg = '登录失败'
            data = '获取授权失败，请确认是否允许授权，并重试。若问题无法解决，请联系网站管理人员'
            return code, msg, data
        infos = github_data['user_info']
        user_email = github_data['user_email']
        nickname = dict_get(infos, 'login')
        image_url = dict_get(infos, 'avatar_url')
        open_id = str(self.oauth_svs.openid)
        signature = dict_get(infos, 'bio')
        if not signature:
            signature = "无个性签名"
        data = {
            'email': user_email,
            'nickname': nickname,
            'image_url': image_url,
            'open_id': open_id,
            'signature': signature
        }

        return Config.CODE_OK, Config.MSG_OK, data
