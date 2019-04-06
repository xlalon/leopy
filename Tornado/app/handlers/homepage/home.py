# -*- coding: utf-8 -*-


from ..base.base_handler import BaseHandler


class HomeHandler(BaseHandler):

    async def get(self):
        args = self.get_params('a', 'b', 'c')
        args_1 = self.get_params(['a', 'b', 'c'])
        args_2 = self.get_params('a', 'b', 'c', dft='', result_type=list)
        args_3 = self.get_params(['a', 'b', 'c'], dft='', result_type=set)

        print('正常获取: ', args, args_1, args_2, args_3)

        return self.render_data(data=args)
