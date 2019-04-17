# -*- coding:utf-8 -*-

from app.handlers.base.base_handler import BaseHandler
from app.services.user.info.info import UserInfoService


class UserInfoHandler(BaseHandler):

    async def get(self):
        uid = self.get_argument('uid', '')
        data = await UserInfoService().user_info_by_uid(uid=uid)
        return self.render_data(data=data)
