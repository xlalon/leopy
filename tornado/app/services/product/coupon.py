# -*- coding: utf-8 -*-

from ..svs_base import BaseService


class ProdCouponSVS(BaseService):

    async def coupon_bind_post(self, headers, body):

        return await self.post(
            domain=self.config.domain,
            path='/v2/promotion/coupon/bindCouponPackage',
            body=body,
            headers=headers)
