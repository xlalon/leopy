# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api

from .info import InfoResource


user_bp = Blueprint('user', __name__, url_prefix='/user')
user = Api(user_bp)


user.add_resource(InfoResource, '/info')
