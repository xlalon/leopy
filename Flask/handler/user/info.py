# -*- coding: utf-8 -*-

from ..base import BaseResource


class InfoResource(BaseResource):

    def get(self):
        return {"Hello": 'Resource'}
