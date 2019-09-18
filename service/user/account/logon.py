#! /usr/bin/env python

from flask import current_app, session
from flask_login import login_user, logout_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from models.user import User
from service.base import BaseService
from service.user.account.info import UserInfoService


class LogonService(BaseService):

    def login(self, username, password):
        """user login"""
        code, msg, data = self.ResponseStatus.CODE_OK, self.ResponseMessages.MSG_OK, None
        # user info
        user = User.query.filter_by(email=username).first()
        # user not exists
        if not user:
            code = self.ResponseStatus.CODE_USER_NOT_EXISTS
            msg = self.ResponseMessages.MSG_USER_NOT_EXISTS
            return code, msg, data
        # password mismatch
        if not user.check_password(password):
            code = self.ResponseStatus.CODE_USER_PASSWORD_MISMATCH
            msg = self.ResponseMessages.MSG_USER_PASSWORD_MISMATCH
            return code, msg, data
        # user's status is not active
        if not user.status:
            code = self.ResponseStatus.CODE_USER_STATUS_INACTIVE
            msg = self.ResponseMessages.MSG_USER_STATUS_INACTIVE
            return code, msg, data
        login_user(user)
        # Tell Flask-Principal the identity changed
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))
        # user info detail
        data = UserInfoService().user_info_get([user.email])
        data = data[0] if data else {}

        return code, msg, data

    def logout(self):
        logout_user()
        # Remove session keys set by Flask-Principal
        for key in ('identity.name', 'identity.auth_type'):
            session.pop(key, None)
        # Tell Flask-Principal the user is anonymous
        identity_changed.send(current_app._get_current_object(),
                              identity=AnonymousIdentity())
        return None
