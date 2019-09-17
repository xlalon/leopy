#! /usr/bin/env python

from models.user import User, UserGroup, UserPermission
from service.base import BaseService


class UserInfoService(BaseService):

    def user_info_add(self, email, username, password, role_id, groups, permissions):
        """new user add
        :param email:        email,      >>>test@sinaif.com
        :param username:     username    >>>Test
        :param password:     password    >>>password9
        :param role_id       role_id     >>>3
        :param groups:       groups      >>>[1, 2, 3]
        :param permissions:  permissions >>>[1, 2, 3]
        """
        # checkout if user exists
        code, msg, data = self.ResponseStatus.CODE_OK, self.ResponseMessages.MSG_OK, None
        if self.is_user_exists(email):
            code = self.ResponseStatus.CODE_USER_EXISTS
            msg = self.ResponseMessages.MSG_USER_EXISTS
            return code, msg, data
        # add user info
        user = User(email=email, username=username, password=password, role_id=role_id)
        self.db.session.add(user)
        self.db.session.flush()
        # user group add
        self.user_group_add(user, groups)
        # user permission add
        self.user_permission_add(user, permissions)

        data = user.to_dict()
        # groups' info of user belong to
        data['groups'] = user.user_groups()
        # permissions' info of user belong to
        data['permissions'] = user.user_permissions()

        self.db.session.commit()

        return code, msg, data

    @staticmethod
    def user_info_get(emails):
        """user info get
        emails should be iterables, eg. [test1@sinaif.com, test2@sinaif.com]
        if not emails, email default set to all in the db, then get info of all users
        """
        if not emails:
            users = User.query.all()
        else:
            users = User.query.filter(User.email.in_(emails)).all()
        data = []
        for user in users:
            info = user.to_dict()
            # groups' info of user belong to
            info['groups'] = user.user_groups()
            # permissions' info of user belong to
            info['permissions'] = user.user_permissions()
            data.append(info)
        return data

    def user_info_update(self, email, username='', password='',
                         role_id=None, status=None, groups=None, permissions=None):
        """
        user info update
        :param email:           email, used to get the user info
        :param username:        username   >>>Test
        :param password:        password   >>>password3
        :param role_id:         role_id    >>>2
        :param status:          status     >>>1
        :param groups:          groups     >>>[1, 2]
        :param permissions:     permission >>>[1, 2]
        """
        code, msg, data = self.ResponseStatus.CODE_OK, self.ResponseMessages.MSG_OK, None
        # check if the user exists, if not, return
        user = self.get_user_from_email(email)
        if not user:
            code = self.ResponseStatus.CODE_USER_NOT_EXISTS
            msg = self.ResponseMessages.MSG_USER_NOT_EXISTS
            return code, msg, data
        # update info
        if username:
            user.username = username
        if password:
            user.password = password
        if role_id:
            user.role_id = role_id
        if status:
            user.status = status
        self.db.session.flush()
        self.user_group_update(user, groups)
        self.user_permission_add(user, permissions)

        data = user.to_dict()
        # groups' info of user belong to
        data['groups'] = user.user_groups()
        # permissions' info of user belong to
        data['permissions'] = user.user_permissions()

        self.db.session.commit()

        return code, msg, data

    def user_group_add(self, user, group_ids):
        """user add groups, group ids should be iterable with ids, such as [1, 2],
        this func does not commit to db, so you should invoke commit later
        """
        if user and group_ids:
            for group in group_ids:
                # exists the group, ignore
                is_exists = UserGroup.query.filter_by(uid=user.id, gid=group).first()
                if is_exists:
                    continue
                user_add_group = UserGroup(uid=user.id, gid=group)
                self.db.session.add(user_add_group)
            self.db.session.flush()

    def user_group_update(self, user, group_ids):
        """user add groups, group ids should be iterable with ids, such as [1, 2],
        this func default delete the groups user had and add the groups_ids,
        so make sure you provide the old groups
        this func does not commit to db, so you should invoke commit later
        """
        if user and group_ids:
            # delete the old groups
            user_delete_groups = UserGroup.query.filter(UserGroup.uid.in_(group_ids)).all()
            for user_group in user_delete_groups:
                self.db.session.delete(user_group)
            self.db.session.flush()
            # add the groups of groups_ids
            for group in group_ids:
                user_add_group = UserGroup(uid=user.id, gid=group)
                self.db.session.add(user_add_group)
            self.db.session.flush()

    def user_permission_add(self, user, permission_ids):
        """user permission add
        this func does not commit to db, so you should invoke commit later
        """
        if user and permission_ids:
            for pid in permission_ids:
                # if user had the permission, ignore
                is_exists = UserPermission.query.filter_by(uid=user.id, pid=pid).first()
                if is_exists:
                    continue
                # add the permission
                user_permission = UserPermission(uid=user.id, pid=pid)
                self.db.session.add(user_permission)
            self.db.session.flush()

    @staticmethod
    def is_user_exists(email):
        """check if user exists, return True if exists or False otherwise"""
        if User.query.filter_by(email=email).first():
            return True
        return False

    @staticmethod
    def get_user_from_email(email):
        user = User.query.filter_by(email=email).first()
        return user
