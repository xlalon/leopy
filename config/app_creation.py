# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_login import LoginManager, current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_principal import Principal, Permission as PrincipalPermission

from models import db
from models.user import Role, User, ADMIN, Permission, UserPermission
from utils.logger import get_logger
from utils.helper import env_config
from utils.exceptions import PermissionDenied

login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(AppConfig)

    db.init_app(app)
    login_manager.init_app(app)
    Principal(app)

    # flask_principal info load
    identity_loader(app)
    # flask_principal permission check
    permission_check(app)
    # record
    request_record(app)
    # blueprint register
    register_bp(app)
    # error handler
    error_handler(app)

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


@login_manager.user_loader
def load_user(user_id):
    # Return an instance of the User model
    return User.query.get(user_id)


def identity_loader(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user
        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        if hasattr(current_user, 'role_id'):
            identity.provides.add(RoleNeed(Role.get(current_user.role_id, 'staff')))


record_logger = get_logger('record')


def request_record(app):
    @app.before_request
    def record():
        record_logger.info(request.path)


def permission_check(app):
    @app.before_request
    def check_perm():
        is_perm_required = Permission.query.filter_by(content_type=request.path).first()
        if is_perm_required:
            permissions = set()
            perm_users = db.session.query(UserPermission.uid)\
                .join(Permission, UserPermission.pid == Permission.id)\
                .filter(Permission.content_type == request.path).all()
            admins = db.session.query(User.id).filter_by(role_id=ADMIN).all()
            for user in perm_users:
                permissions.add(UserNeed(user.uid))
            for user in admins:
                permissions.add(UserNeed(user.id))
            if not PrincipalPermission(*permissions).can():
                raise PermissionDenied('PermissionDenied.')


def error_handler(app):
    @app.errorhandler(PermissionDenied)
    def permission_denied_handler(error):
        return PermissionDenied().to_json(msg=error.msg)
