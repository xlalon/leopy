# -*- coding: utf-8 -*-

from app.services.product.search import ProdSearchSVS
from app.handlers.base.base_handler import BaseHandler


class WordSearchHandler(BaseHandler):

    async def get(self):
        is_force = self.get_query_argument('is_force')
        keywords = self.get_query_argument('keywords')
        limit = self.get_query_argument('limit', 5)
        sort = self.get_query_argument('sort', 0)

        query = {'is_force': is_force, 'keywords': keywords, 'limit': limit, 'sort': sort}

        data = await ProdSearchSVS().prod_by_search_word_get(headers=self.headers, query=query)
        return self.render_data(chuck=data)
