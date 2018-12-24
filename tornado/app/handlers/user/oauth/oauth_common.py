# -*- coding: utf-8 -*-


from app.businesses.user.account import AccountBusiness
from app.handlers.base.base_handler import BaseHandler


class CommonLoginHandler(BaseHandler):

    async def post(self):
        email = self.get_body_argument('email', '')
        password = self.get_body_argument('password', '')
        token = self.get_body_argument('token', '')
        code, msg, data = await AccountBusiness().common_login(
            email=email,
            password=password,
            token=token,
            mysql_db=self.mysql_db)

        return self.render_data(code=code, msg=msg, data=data)
