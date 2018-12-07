# -*- coding: utf-8 -*-

from ..base.base_business import BaseBusiness


class HelloWorldBusiness(BaseBusiness):

    async def gain_hello_world(self):

        # self.redis_db.zadd('zset-key:a', {'c': 30, 'd': 40})
        # self.redis_db.expire('zset-key:a', 100)
        aa = self.redis_db.zrange('zset-key:a', 0, -1, withscores=True)
        aa = [(a.decode('utf8'), b) for a, b in aa]

        return aa
