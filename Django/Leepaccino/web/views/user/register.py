# -*- coding: utf-8 -*-

from passlib.hash import bcrypt
from time import time

from .. import helper, config
from ..base import BaseHandler
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserRegisterHandler(BaseHandler):

    def post(self, request):
        pass
