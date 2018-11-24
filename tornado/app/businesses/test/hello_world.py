# -*- coding: utf-8 -*-

from ..base.base_business import BaseBusiness


class HelloWorldBusiness(BaseBusiness):

    async def gain_hello_world(self):
        hello_world_data = await self.hello_world_svs.get_hello_world()
        hello_world_data['Hello'] = 'www.hello_world.com'
        return '0', hello_world_data
