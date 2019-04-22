# -*- coding: utf-8 -*-

from flask import Blueprint

from .info import InfoView


user = Blueprint('user', __name__, url_prefix='/user')

user_urls = (
    ('info', InfoView, 'info'),
)
