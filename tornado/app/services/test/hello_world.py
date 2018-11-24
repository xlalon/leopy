# -*- coding: utf-8 -*-
"""
数据源
"""

from ..base.base_service import BaseService


class HelloWorldService(BaseService):

    @staticmethod
    async def get_hello_world():
        return {'Hello': 'World!!!'}
