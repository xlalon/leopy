# -*- coding: utf-8 -*-

from ..base import BaseModelService
from models.user.account import UserLoginModel


class AccountService(BaseModelService):

    def login_service(self):
        user_leo_ins = UserLoginModel.query.filter_by(user_name='leo').first()

        need_attr = ['user_name', 'attr_test']
        value_default = 'Default Value'
        user_leo = self.model2_dict(user_leo_ins, need_attr, default=value_default)

        return user_leo
