# -*- coding: utf-8 -*-

from ..BaseView import BaseView

from flask import jsonify


class InfoView(BaseView):

    def get(self):
        from flask import current_app, request, g
        g.name = 1
        return jsonify({'user': 'info'})
