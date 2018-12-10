# -*- coding: utf-8 -*-

from app.handlers.base.base_handler import BaseHandler
from app.services.product.coupon import ProdCouponSVS


class CouponBindHandler(BaseHandler):

    async def post(self):
        coupon_pack_id = self.get_body_argument('couponPackId')
        version = self.get_body_argument('version', 'v2')
        body = {
            'couponPackId': coupon_pack_id,
            'version': version
        }
        data = await ProdCouponSVS().coupon_bind_post(headers=self.headers, body=body)
        return self.render_data(chuck=data)
