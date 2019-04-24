# -*- coding: utf-8 -*-

from flask import Flask
from views import bp_and_urls


def create_app(mode):
    """创建app工厂方法"""

    app = Flask(__name__)

    # 加载配置
    config = load_config(mode)
    app.config.from_object(config)

    # 加载蓝图
    load_blueprint(app)

    return app


def load_config(mode):
    if mode == 'product':
        from settings import ProductConfig
        return ProductConfig
    else:
        from settings import TestConfig
        return TestConfig


def load_blueprint(app):
    """加载蓝图"""
    for bp, urls in bp_and_urls:
        # 蓝图路由
        load_urls(urls, bp)
        # 注册蓝图
        app.register_blueprint(bp)


def load_urls(urls, blueprint):
    """加载蓝图路由"""
    for url, view, view_name in urls:
        blueprint.add_url_rule(url, view_func=view.as_view(view_name))
