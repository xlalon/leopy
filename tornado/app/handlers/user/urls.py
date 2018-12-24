# -*- coding: utf-8 -*-

from .oauth import *

urls = [
    # github登录路由
    (r'oauth/github_login', GithubOauthHandler),
    # github登录回调
    (r'oauth/github_check', GithubOauthHandler),
    # common_register
    (r'oauth/account_register', AccountRegisterHandler),
    # common_login
    (r'oauth/common_login', CommonLoginHandler),
]
