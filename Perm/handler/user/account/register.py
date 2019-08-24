#! /usr/bin/env python

from handler.base import BaseHandler
from service.user.account.info import UserInfoService


class RegisterHandler(BaseHandler):
    def post(self):
        # email & username & password & groups & permissions
        # username default trans to capitalize, if username not provide, default set to email prefix
        # password's length should between 6 and 20 and begin with alpha, otherwise raise ValidationError
        # if provide groups, groups should be type of str split with ',' such as '1,2,3'
        # if provide permissions, permissions should be type of str split with ',' such as '1,2,3'
        # email
        email = self.get_argument('email')
        # username
        username = self.get_argument('username', '')
        if not username:
            username = email.split('@')[0]
        username = username.capitalize()
        # password
        password = self.get_argument('password')
        # role_id default staff
        role_id = self.get_argument('role_id', 3, type_=int)
        # groups
        groups = self.get_argument('groups', '')
        groups = [int(id_) for id_ in groups.split(',')] if groups else []
        # permissions
        permissions = self.get_argument('permissions', '')
        permissions = [int(id_) for id_ in permissions.split(',')] if permissions else []
        # business data
        code, msg, data = UserInfoService().user_info_add(
            email=email,
            username=username,
            password=password,
            role_id=role_id,
            groups=groups,
            permissions=permissions)

        return self.render_data(code=code, msg=msg, data=data)
