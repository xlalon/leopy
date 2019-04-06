# -*- coding: utf-8 -*-

from app.businesses.test.hello_world import HelloWorldBusiness
from ..base.base_handler import BaseHandler


class HelloWorldHandler(BaseHandler):

    async def get(self):
        args = self.get_req_args('a', 'b', 'c', default='')
        print('正常获取: ', args)

        args_1 = self.get_req_args('a', 'b', 'c', args_alias=['A', 'B', 'C'], default='ABCDEFG')
        print('参数和自定义参数名字一一对应: ', args_1)

        args_2 = self.get_req_args(['a', 'c'], args_alias={'a': 'A'}, default='1000')
        print('更改特定参数名字: ', args_2)

        arg_a = args.a
        print('通过属性获取参数: ', arg_a)

        args_3 = self.get_req_args('a', 'b', 'c')
        print('不加default， 缺少参数时引发异常', args_3)

        data = await HelloWorldBusiness(redis_db=self.redis_db).gain_hello_world(args)
        return self.render_data(data=data)
