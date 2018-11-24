# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from .account import UserLoginHandler
from .point import UserPointHandler


urls = [
    (r'account/login', UserLoginHandler),
    (r'point/point', UserPointHandler)
]
