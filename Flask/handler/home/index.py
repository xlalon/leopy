# -*- coding: utf-8 -*-

from ..base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):

        return self.render_data(dict(Location='Homepage'))
