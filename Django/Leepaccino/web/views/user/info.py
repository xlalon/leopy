# -*- coding: utf-8 -*-

from datetime import datetime
from .. import User
from ..base import BaseView


class UserInfoView(BaseView):

    def get(self, request):
        """User information gain"""
        username = self.get_argument('user')
        user = User.objects.filter(username=username).first()
        username = user.username if user else ''
        username = username.capitalize()
        context = {'user': username, 'time': datetime.now()}
        return self.render_html('user_info.html', context)

    def post(self, request):
        """User information update"""
        pass
