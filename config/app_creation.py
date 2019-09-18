# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_login import LoginManager

from models import db
from utils.logger import get_logger
from utils.helper import env_config

login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(AppConfig)

    db.init_app(app)
    login_manager.init_app(app)

    before_after_request(app)
    register_bp(app)

    return app


class AppConfig:
    DEBUG = env_config('DEBUG', eval_=True)
    SECRET_KEY = env_config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = env_config('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def register_bp(app):
    from handler.home import home_bp
    from handler.user import user_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)


record_logger = get_logger('record')


def before_after_request(app):
    @app.before_request
    def record():
        record_logger.info(request.path)
