#! /usr/bin/env python

from collections import defaultdict

from models.user import Permission
from service.base import BaseService


class PermissionService(BaseService):

    @staticmethod
    def permission_get(permissions_ids):
        """permission list"""
        data = defaultdict(list)
        if not permissions_ids:
            permissions = Permission.query.all()
        else:
            permissions = Permission.query.filter(Permission.id.in_(permissions_ids)).all()
        # trans to typed data structure
        for p in permissions:
            name_prefix, name_suffix = p.name.split('_')
            p_data = p.to_dict()
            p_data['name'] = name_suffix
            data[name_prefix].append(p_data)
        return data

    def permission_add(self, code, name, content_type):
        """
        permission add
        :param code:
        :param name:
        :param content_type:
        """
        p = Permission(code=code, name=name, content_type=content_type)
        self.db.session.add(p)
        self.db.session.commit()

    def permission_update(self, pid, code, name, content_type):
        """
        permission update
        :param pid:         id of permission
        :param code:
        :param name:
        :param content_type:
        """
        permission = self.get_permission_from_id(pid)
        if not permission:
            return
        if code:
            permission.code = code
        if name:
            permission.name = name
        if content_type:
            permission.content_type = content_type
        self.db.session.commit()

    def permission_delete(self, pid):
        Permission.query.filter_by(id=pid).delete()
        self.db.session.commit()

    @staticmethod
    def get_permission_from_id(pid):
        permission = Permission.query.get(id=pid)
        return permission
