#! /usr/bin/env python

from handler.base import BaseHandler
from service.user.account.logon import LogonService


class LoginHandler(BaseHandler):

    def post(self):
        """user login via name and password"""
        username = self.get_argument('name')
        password = self.get_argument('password')

        code, msg, data = LogonService().login(username=username, password=password)

        return self.render_data(data=data, msg=msg, code=code)


class LogoutHandler(BaseHandler):

    def get(self):
        data = LogonService().logout()
        return self.render_data(data=data)
