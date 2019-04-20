# -*- coding: utf-8 -*-

from ..base.base_handler import BaseHandler


class TestHandler(BaseHandler):

    async def get(self):
        data = {'test': 'test'}
        return self.render_data(data=data)
