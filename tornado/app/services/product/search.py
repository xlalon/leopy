# -*- coding:utf-8 -*-

from ..svs_base import BaseService


class ProdSearchSVS(BaseService):

    async def prod_by_search_word_get(self, headers, query):
        return await self.get(
            domain=self.config.domain,
            path='/v2/Product/search/getSearchProducts',
            query=query,
            headers=headers)
