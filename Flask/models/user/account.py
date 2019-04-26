# -*- coding: utf-8 -*-

from .. import db


class UserLoginModel(db.Model):
    """用户登录"""
    __tablename__ = 'user_login'

    uid = db.Column(db.Integer, primary_key=True, comment='用户id')
    user_name = db.Column(db.String(24), nullable=False, comment='用户名')
    email = db.Column(db.String(64), nullable=False, comment='用户邮箱')
    password = db.Column(db.String(128), nullable=False, comment='用户密码')
    token = db.Column(db.String(256), nullable=False, comment='登录token')
    user_state = db.Column(db.Integer, nullable=False, default=1, comment='登录状态')
