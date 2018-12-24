# -*- coding: utf-8 -*-

from app.handlers.base.base_handler import BaseHandler
from app.businesses.user.account import AccountBusiness


class AccountRegisterHandler(BaseHandler):

    async def post(self):
        email = self.get_body_argument('email')
        password = self.get_body_argument('password')
        nickname = self.get_body_argument('nickname')
        realname = self.get_body_argument('realname', '')
        gender = self.get_body_argument('gender', 'M')
        birthday = self.get_body_argument('birthday', 0)
        code, msg, data = await AccountBusiness().common_register(
            email=email,
            password=password,
            nickname=nickname,
            realname=realname,
            gender=gender,
            birthday=birthday,
            mysql_db=self.mysql_db)

        return self.render_data(code=code, msg=msg, data=data)
