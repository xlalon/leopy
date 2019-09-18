#! /usr/bin/env python

from handler.base import BaseHandler, admin_permission
from service.user.account.info import UserInfoService


class CheckUserExistsHandler(BaseHandler):
    def get(self):
        """check if user exists via email"""
        email = self.get_argument('email')
        data = UserInfoService().is_user_exists(email)
        data = {'result': 1 if data else 0}
        return self.render_data(data=data)


class UserInfoHandler(BaseHandler):
    @admin_permission.require(403)
    def get(self):
        """user info"""
        # emails split with ',', eg. 'test1@sinaif.com,test2@sinaif.com'
        # if not provide, return all users' info
        email = self.get_argument('email', '')
        if email:
            email = email.split(',')
        else:
            email = []
        data = UserInfoService().user_info_get(email)
        return self.render_data(data)

    @admin_permission.require(403)
    def post(self):
        """user info update"""
        # email, used to get user info, must.
        email = self.get_argument('email')
        # username & password, optional
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        # role id
        role_id = self.get_argument('role_id', None)
        if role_id is not None:
            role_id = int(role_id)
        # user account status 0(inactive)/1(active)
        status = self.get_argument('status', None)
        if status is not None:
            status = int(status)
        # group ids, str split with ',', eg, '1,2,3'
        groups = self.get_argument('groups', '')
        if groups:
            groups = [int(id_) for id_ in groups.split(',')]
        # permission ids, str split with ',', eg, '1,2,3'
        permissions = self.get_argument('permissions', '')
        if permissions:
            permissions = [int(id_) for id_ in permissions.split(',')]

        code, msg, data = UserInfoService().user_info_update(
            email=email,
            username=username,
            password=password,
            role_id=role_id,
            status=status,
            groups=groups,
            permissions=permissions)

        return self.render_data(code=code, msg=msg, data=data)
