# -*- coding: utf-8 -*-

from passlib.hash import bcrypt
from time import time

from .. import User
from .. import helper, config
from ..base import BaseHandler


class UserRegisterHandler(BaseHandler):

    def post(self, request):
        # Add a new user
        email = self.get_argument('email')
        if not helper.verify_email(email):
            return self.render_json(
                code=config.Code.EMAIL_FAIL,
                msg='Please make sure the invalidation of email address!')

        username = helper.un_from_email(email)
        password = self.get_argument('password')
        token_db = bcrypt.hash(password)
        n_time = str(int(time()))

        user = User(email=email,
                    token=token_db,
                    username=username,
                    join_time=n_time)
        result = helper.db_insert(user)
        response = 'The email had been Registered!'
        if result:
            token = self._gen_token(token_db)
            response = dict(id=user.id,
                            email=user.email,
                            token=token,
                            username=user.username,
                            join_time=user.join_time)
        # user_t = Thread(target=helper.db_insert, args=(user, ))
        # user_t.start()
        # user_t.join()

        return self.render_json(data=response)
