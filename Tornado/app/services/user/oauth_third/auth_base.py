# -*- coding: utf-8 -*-

from app.services.svs_base import BaseService


class OAuthBase(BaseService):
    """第三方登录基类"""

    def __init__(self, client_id, client_key, redirect_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    # 下面的方法，不同的登录平台会有细微差别，需要继承基类后重写方法
    async def get_auth_url(self):
        pass

    async def get_access_token(self, code):
        pass

    async def get_open_id(self):
        pass

    async def get_user_info(self):
        pass

    async def get_email(self):
        pass

