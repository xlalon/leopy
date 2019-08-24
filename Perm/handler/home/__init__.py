# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api

from .index import IndexHandler


home_bp = Blueprint('home', __name__)
user = Api(home_bp)


user.add_resource(IndexHandler, '/')
