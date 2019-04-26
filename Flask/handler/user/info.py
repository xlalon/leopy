# -*- coding: utf-8 -*-

from ..base import BaseHandler
from service.models.user.account import AccountService


class InfoHandler(BaseHandler):

    def get(self):
        user_loe = AccountService().login_service()
        return self.render_data(user_loe)
