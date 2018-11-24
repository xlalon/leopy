# -*- coding: utf-8 -*-

from ..base.base_handler import BaseHandler


class UserLoginHandler(BaseHandler):

    async def get(self):
        return self.render_data(
            code='0',
            data={
                'username': 'Leo', 'sex': 'man'
            }
        )
