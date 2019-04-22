# -*- coding: utf-8 -*-

from flask.views import MethodView


class BaseView(MethodView):

    def render_data(self):
        pass
