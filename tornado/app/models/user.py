# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Enum
from .import Base


class User(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(64), nullable=False, unique=True)
    realname = Column(String(64), nullable=True)
    sex = Column(Enum('x', 'o'), nullable=True)
    age = Column(Integer, nullable=True)
    join_time = Column(String(64))
