# -*- coding: utf-8 -*-

from .base import BaseTestCase


class ProdTestCase(BaseTestCase):

    def test_prod(self):
        res = self.get(
            '/product/search/products_by_search_word',
            query={'is_force': True, 'keywords': 'black'},
            headers=self.headers
        )
        self.assertEqual(res.code, 200)
        data = self.res2_data(res)
        self.assertEqual(data.info.num, 0)
