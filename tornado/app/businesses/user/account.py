# -*- coding: utf-8 -*-

from time import time
from itsdangerous import URLSafeSerializer
from sqlalchemy import or_

from app.models.user import Users
from config import Config


class AccountBusiness:

    def __init__(self):
        self.auth_s = URLSafeSerializer(Config.secret_key, 'account')

    async def common_register(self, *, email, password, nickname, realname, gender, birthday, mysql_db):
        # 查看数据库是否存在email or nickname, 存在返回错误，提示更换别的email或者nickname
        user = mysql_db.query(Users).filter(or_(
            Users.email == email, Users.nickname == nickname)).first()
        if user:
            return Config.CODE_ACCOUNT_EXIST, Config.MSG_ACCOUNT_EXIST, None
        # 计算token， 存库。
        token = self.auth_s.dumps({"email": email, "password": password})
        now = int(time())
        user = Users(
            email=email,
            token=token,
            nickname=nickname,
            realname=realname,
            gender=gender,
            birthday=birthday,
            join_time=now,
            update_time=now
        )
        with mysql_db.begin():
            mysql_db.add(user)

        return Config.CODE_OK, Config.MSG_OK, None

    async def common_login(self, *, email, password, token, mysql_db):
        user = None
        if token:
            user = mysql_db.query(Users).filter_by(token=token).first()
        if all([not user, email, password]):
            # 如果token登录失败, 尝试email&password登录, 使用email&password计算出token值
            token = self.auth_s.dumps({"email": email, "password": password})
            user = mysql_db.query(Users).filter_by(token=token).first()
        if user:
            # 和记录一致，允许登录
            if self.auth_s.loads(token).get('email') == user.email:
                data = {
                    'email': user.email,
                    'nickname': user.nickname,
                    'token': token
                }
                return Config.CODE_OK, Config.MSG_OK, data
        else:
            # token和email&password 均登录失败
            return Config.CODE_PAGE_NOT_FOUND, Config.MSG_ACCOUNT_WRONG, None
