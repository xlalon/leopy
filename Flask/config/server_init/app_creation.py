# -*- coding: utf-8 -*-

from flask import Flask

from handler.user import user_bp
from handler.home import home_bp
from config.settings import ENV_CONFIG


def create_app():

    app = Flask(__name__)
    app.config.from_object(load_config())

    register_bp(app)

    return app


def load_config():
    mode = ENV_CONFIG['APP_ENV']
    if mode == 'product':
        from config.settings import ProDeConfig
        return ProDeConfig
    else:
        from config.settings import DevDeConfig
        return DevDeConfig


def register_bp(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
