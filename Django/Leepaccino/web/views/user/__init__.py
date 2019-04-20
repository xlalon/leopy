# -*- coding: utf-8 -*-

from django.urls import path
from .info import UserInfoView
from .register import UserRegisterHandler
from .login import CommonLoginHandler


urls_user = [
    path('user/info', UserInfoView.as_view(), name='user_info'),
    path('user/register', UserRegisterHandler.as_view(), name='user_register'),
    path('user/common_login', CommonLoginHandler.as_view(), name='common_login'),
]
