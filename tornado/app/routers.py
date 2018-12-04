# -*- coding: utf-8 -*-

import tornado.web
from importlib import import_module
from app.utils.decoraters import url_wrapper


def include(module):
    res = import_module(module)
    return getattr(res, 'urls', res)


def load_settings(mode):
    return dict(
        debug=mode != 'product'
    )


def make_app():
    return tornado.web.Application(url_wrapper([
        (r"/user/", include('app.handlers.user.urls')),
    ]), **load_settings(mode='test'))
