# -*- coding: utf-8 -*-

from app.businesses.test.hello_world import HelloWorldBusiness
from ..base.base_handler import BaseHandler


class HelloWorldHandler(BaseHandler):

    async def get(self):
        code, data = await HelloWorldBusiness().gain_hello_world()
        return self.render_data(code=code, data=data)
