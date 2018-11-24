# -*- coding: utf-8 -*-

from functools import wraps, partial


def data_monitor(func=None, default=None):
    """数据开关
    :param func
    :param default
    """
    # 参数可选支持
    if func is None:
        return partial(data_monitor, default=default)

    @wraps(func)
    async def _(*args, **kwargs):
        try:
            data = await func(*args, **kwargs)
        except:
            return default() if callable(default) else default
        else:
            return data
    return _


if __name__ == '__main__':

