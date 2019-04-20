# -*- coding: utf-8 -*-

from app.handler.product.search.word_search import WordSearchHandler
from app.handler.product.coupon.coupon_bind import CouponBindHandler

urls = [
    # 搜索商品
    (r'search/products_by_search_word', WordSearchHandler),
    # 优惠券绑定
    (r'coupon/bind', CouponBindHandler),
]
