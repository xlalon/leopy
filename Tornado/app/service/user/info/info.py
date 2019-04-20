# -*- coding:utf-8 -*-

from app.models.user import Users
from app.services.svs_base import BaseService
from app.utils.db import db_ins2dict


class UserInfoService(BaseService):

    async def user_info_by_uid(self, uid):
        user = self.mysql_db.query(Users).filter_by(id=uid).first()
        user = db_ins2dict(user)
        return user
