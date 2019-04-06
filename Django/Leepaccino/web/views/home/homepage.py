# -*- coding: utf-8 -*-

from ..base import BaseView


class HomeView(BaseView):
    """主页"""

    template_name = 'home.html'

    def get(self, request):

        return self.render_html(self.template_name)
