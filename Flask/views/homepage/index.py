# -*- coding: utf-8 -*-

from ..BaseView import BaseView


class IndexView(BaseView):

    def get(self):
        return 'Hello View'
