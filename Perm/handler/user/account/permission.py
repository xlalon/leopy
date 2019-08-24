#! /usr/bin/env python

from handler.base import BaseHandler
from service.user.account.permission import PermissionService


class PermissionHandler(BaseHandler):

    def get(self):
        """permission list"""
        # permission id, str split with `,`, eg. '1,2,3'
        # if not provide, return all permissions
        pid = self.get_argument('pid', [])
        if pid:
            pid = [int(id_) for id_ in pid]

        data = PermissionService().permission_get(pid)

        return self.render_data(data=data)

    def post(self):
        code = self.get_argument('code')
        name = self.get_argument('name')
        content_type = self.get_argument('content_type', '')

        data = PermissionService().permission_add(code, name, content_type)

        return self.render_data(data)
