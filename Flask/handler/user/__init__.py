#! /usr/bin/env python

from flask import Blueprint
from flask_restful import Api

from .account.logon import LoginHandler, LogoutHandler
from .account.register import RegisterHandler
from .account.info import CheckUserExistsHandler
from .account.info import UserInfoHandler
from .account.permission import PermissionHandler

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_api = Api(user_bp)

# common login & logout
user_api.add_resource(LoginHandler, '/login')
user_api.add_resource(LogoutHandler, '/logout')
# add user/register
user_api.add_resource(RegisterHandler, '/add_user')
# check if user exists
user_api.add_resource(CheckUserExistsHandler, '/check_user_exists')
# user info get/update
user_api.add_resource(UserInfoHandler, '/info')
# permission get/add
user_api.add_resource(PermissionHandler, '/permission')
