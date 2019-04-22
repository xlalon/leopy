# -*- coding: utf-8 -*-

from flask import Blueprint

from .index import IndexView


homepage = Blueprint('homepage', __name__)

homepage_urls = (
    ('/', IndexView, 'index'),
)
