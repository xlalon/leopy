# -*- coding: utf-8 -*-

from ..base.base_handler import BaseHandler
from config import Config


class UserPointHandler(BaseHandler):

    async def get(self):
        username = 'Leo'
        user_id = '001'
        return self.render_data(
            code=Config.CODE_OK,
            data={
                'user_id': user_id,
                'username': username,
                'point': 99
            }
        )
