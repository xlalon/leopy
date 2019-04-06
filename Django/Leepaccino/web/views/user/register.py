# -*- coding: utf-8 -*-

from passlib.hash import bcrypt
from time import time

from .. import helper, config
from ..base import BaseHandler


class UserRegisterHandler(BaseHandler):

    def post(self, request):
        pass
