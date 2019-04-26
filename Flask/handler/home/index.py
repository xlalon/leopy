# -*- coding: utf-8 -*-

from ..base import BaseResource


class IndexResource(BaseResource):

    def get(self):

        return {'Hello': 'Index'}
