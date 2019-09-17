# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager

from config.settings import ENV_CONFIG
from handler.home import home_bp
from models import db

login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(load_config())

    db.init_app(app)
    login_manager.init_app(app)

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
    from handler.user import user_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
