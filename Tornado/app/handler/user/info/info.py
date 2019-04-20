# -*- coding:utf-8 -*-

from app.handler.base.base_handler import BaseHandler
from app.service.user.info.info import UserInfoService


class UserInfoHandler(BaseHandler):

    async def get(self):
        uid = self.get_argument('uid', '')
        data = await UserInfoService().user_info_by_uid(uid=uid)
        return self.render_data(data=data)
