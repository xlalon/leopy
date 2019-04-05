# -*- coding: utf-8 -*-

from ..base import BaseHandler


class CommonLoginHandler(BaseHandler):

    def post(self, request):
        token = self.get_argument('token', '')
        email, password = self.get_arguments(['email', 'password'], default='')
        user_info = self.get_user(request, email=email, password=password, token=token)
        return self.render_json(data=user_info)
