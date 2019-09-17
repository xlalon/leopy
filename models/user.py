#! /usr/bin/env python

from collections import defaultdict
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256

from . import db


ADMIN = 1
LEADER = 2
STAFF = 3
Role = {ADMIN: 'admin', LEADER: 'leader', STAFF: 'staff'}


class User(db.Model, UserMixin):
    __tablename__ = 'u_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(256))
    role_id = db.Column(db.Integer, default=3)
    status = db.Column(db.Integer, default=0)

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
    __tablename__ = 'u_group'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64))
    name = db.Column(db.String(64))


class UserGroup(db.Model):
    __tablename__ = 'u_user_group'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    gid = db.Column(db.Integer)


class Permission(db.Model):
    __tablename__ = 'u_permission'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64))
    name = db.Column(db.String(64))
    content_type = db.Column(db.String(256), nullable=False, default='')


class UserPermission(db.Model):
    __tablename__ = 'u_user_permission'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
