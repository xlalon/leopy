#! /usr/bin/env python

from collections import defaultdict
from flask_login import UserMixin
from sqlalchemy import func
from passlib.hash import pbkdf2_sha256

from . import db


ADMIN = 1
LEADER = 2
STAFF = 3
Role = {ADMIN: 'admin', LEADER: 'leader', STAFF: 'staff'}


class User(db.Model, UserMixin):
    """
    CREATE TABLE u_user(
    id INT auto_increment PRIMARY KEY COMMENT '用户表id',
    email VARCHAR(64) NOT NULL COMMENT 'email地址',
    phone VARCHAR(16) NOT NULL DEFAULT '' COMMENT '手机',
    username VARCHAR(64) NOT NULL DEFAULT '' COMMENT '用户名,默认为邮箱前缀',
    password_hash VARCHAR(256) NOT NULL COMMENT '用户密码',
    role_id tinyint NOT NULL DEFAULT 3 COMMENT '用户角色id, 1:admin 2:leader, 3:staff',
    status tinyint NOT NULL default 0 COMMENT '用户账号状态, 0:未激活, 1:激活',
    join_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建账号时间',
    UNIQUE KEY email(email),
    KEY join_time(join_time)
    )engine=Innodb charset=utf8 COMMENT '用户表';
    """
    __tablename__ = 'u_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(16), nullable=False, default='')
    username = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, default=3)
    status = db.Column(db.Integer, default=0)
    join_time = db.Column(db.DATETIME, server_default=func.now())

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, passwd):
        self.password_hash = pbkdf2_sha256.hash(passwd)

    def check_password(self, passwd):
        return pbkdf2_sha256.verify(passwd, self.password)

    def user_groups(self):
        if self.role_id == ADMIN:
            groups = Group.query.all()
        else:
            groups = db.session.query(Group)\
                .join(UserGroup, Group.id == UserGroup.gid)\
                .join(User, UserGroup.uid == User.id)\
                .filter(User.id == self.id).all()
        groups = [g.to_dict() for g in groups]
        return groups

    def user_permissions(self):
        permissions_data = defaultdict(list)
        if self.role_id == ADMIN:
            permissions = Permission.query.all()
        else:
            permissions = db.session.query(Permission)\
                .join(UserPermission, Permission.id == UserPermission.pid)\
                .join(User, UserPermission.uid == User.id)\
                .filter(User.id == self.id).all()
        for p in permissions:
            name_prefix, name_suffix = p.name.split('_')
            p_data = p.to_dict()
            p_data['name'] = name_suffix
            permissions_data[name_prefix].append(p_data)

        return permissions_data


class Group(db.Model):
    """
    CREATE TABLE u_group(
    id int auto_increment PRIMARY KEY COMMENT '产品组id',
    code VARCHAR(64) NOT NULL COMMENT '组code',
    name VARCHAR(64) NOT NULL COMMENT '组name',
    UNIQUE KEY codename(code, name)
    )engine=Innodb charset=utf8 COMMENT '用户组表';
    """
    __tablename__ = 'u_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)


class UserGroup(db.Model):
    """
    CREATE TABLE u_user_group(
    id INT auto_increment PRIMARY KEY COMMENT '主键id',
    uid INT NOT NULL COMMENT '关联的用户id',
    gid INT NOT NULL COMMENT '关联的组id',
    UNIQUE KEY ugid(uid, gid)
    )engine=Innodb charset=utf8 COMMENT '用户所属组别表';
    """
    __tablename__ = 'u_user_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False)
    gid = db.Column(db.Integer, nullable=False)


class Permission(db.Model):
    """
    CREATE TABLE u_permission(
    id INT auto_increment PRIMARY KEY COMMENT '主键id',
    code VARCHAR(64) NOT NULL COMMENT '权限码',
    name VARCHAR(64) NOT NULL COMMENT '权限名',
    content_type VARCHAR(256) NOT NULL DEFAULT '' COMMENT '权限对应的资源',
    UNIQUE KEY codename(code, name)
    )engine=Innodb charset=utf8 COMMENT '权限表';
    """
    __tablename__ = 'u_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    content_type = db.Column(db.String(256), nullable=False, default='')


class UserPermission(db.Model):
    """
    CREATE TABLE u_user_permission(
    id INT auto_increment PRIMARY KEY COMMENT '主键id',
    uid INT NOT NULL COMMENT '关联的用户id',
    pid INT NOT NULL COMMENT '关联的权限id',
    UNIQUE KEY upid(uid, pid)
    )engine=Innodb charset=utf8 COMMENT '用户权限表';
    """
    __tablename__ = 'u_user_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
