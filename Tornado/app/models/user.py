# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Enum
from .import Base


class Users(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(64), nullable=False)
    token = Column(String(128), nullable=False)
    nickname = Column(String(64), nullable=False, unique=True)
    realname = Column(String(64), nullable=False, default='')
    gender = Column(Enum('M', 'F'), nullable=False)
    birthday = Column(Integer, nullable=False, default=0)
    join_time = Column(Integer, nullable=False)
    update_time = Column(Integer, nullable=False)
