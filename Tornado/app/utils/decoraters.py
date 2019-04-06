# -*- coding: utf-8 -*-

import inspect
from functools import partial, wraps

SWITCH = True


def url_wrapper(urls):
    """路由装饰器"""
    wrapper_list = []
    for url in urls:
        path, handles = url
        if isinstance(handles, (tuple, list)):
            for handle in handles:
                pattern, handle_class = handle
                wrap = ('{0}{1}'.format(path, pattern), handle_class)
                wrapper_list.append(wrap)
        else:
            wrapper_list.append((path, handles))
    return wrapper_list


def data_switch(func=None, default=None, switch=SWITCH):
    """数据开关
    :param func
    :param default
    :param switch     值为False开启
    """
    # 参数可选支持
    if func is None:
        return partial(data_switch, default=default, switch=switch)

    @wraps(func)
    async def _(*args, **kwargs):
        if switch is False:
            # 返回默认值（可为值或者可调用对象）
            return default() if callable(default) else default
        return await func(*args, **kwargs)
    return _


def data_monitor(func=None, default=None, switch=SWITCH):
    """数据开关
    :param func
    :param default
    :param switch  值为False开启
    """
    # 参数可选支持
    if func is None:
        return partial(data_monitor, default=default, switch=switch)

    @wraps(func)
    async def _(*args, **kwargs):
        if switch is False:
            try:
                return await func(*args, **kwargs)
            except:
                return default() if callable(default) else default
        else:
            return await func(*args, **kwargs)
    return _


def type_assert(*ty_args, **ty_kwargs):
    """强制参数类型检查
    [In]:  @type_assert(int, c=str)
     ...:  def test_type_assert(a, b, c):
     ...:      print(a, b, c)
    [In]:  test_type_assert(1, 2, 'a')                                  # 类型正确使用
    [Out]: 1 2 a                                                        # 正常输出
    [In]:  test_type_assert(1, 2, 3)                                    # 类型错误使用
    [Out]: TypeError: test_type_assert arg `c` expect `str`, got `int`  # 引发异常
    """
    def wrapper(func):
        sig = inspect.signature(func)
        # 类型松散绑定
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def _(*args, **kwargs):
            # 函数参数全绑定
            bound_values = sig.bind(*args, **kwargs).arguments
            for name, value in bound_values.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('{} arg `{}` expect `{}`, got `{}`'.format(
                            func.__name__, name, bound_types[name].__name__, type(value).__name__))
            return func(*args, **kwargs)
        return _
    return wrapper


@type_assert(int, c=str)
def test_type_assert(a, b, c):
    print(a, b, c)


TYPE = (str, int, float, list, set, dict, tuple, type(None), bool)


def data_type_check(data, data_type):
    def wrong_type_tip(data_, type_):
        if not isinstance(data_, type_):
            print('Item `{}` expect {},  got {}'.format(data_, type_.__name__,  type(data_).__name__))
    try:
        if data_type in TYPE:
            wrong_type_tip(data, data_type)
        elif isinstance(data_type, (list, tuple)):
            for idx, item in enumerate(data_type):
                if item in TYPE:
                    wrong_type_tip(data[idx], item)
        elif isinstance(data_type, dict):
            for k, v in data_type.items():
                if k not in data:
                    print('Key `{}` not in {}'.format(k, data))
                    continue
                if v in TYPE:
                    wrong_type_tip(data[k], v)
                elif isinstance(v, dict):
                    data_type_check(data[k], v)
                elif isinstance(v, (list, tuple)):
                    if len(v) == 1 and isinstance(v[0], dict):
                        for item in data[k]:
                            data_type_check(item, v[0])
                    else:
                        for idx, item in enumerate(v):
                            data_type_check(data[k][idx], item)
    except (KeyError, IndexError, TypeError) as e:
        print('data_type_check failed: ', e)


if __name__ == '__main__':
    pass
    # test_type_assert(1, 2, 'a')
    # test_type_assert(1, 2, 3)

    # data_t = {
    #     'key_a': {'v_a1': int, 'v_a2': str, 'v_a3': list, 'v_a4': dict},
    #     'key_b': [
    #         {'v_b5': {'v_b55': int}},
    #         {'v_b6': [int, str]},
    #         {'v_b7': [{'v_b77': int}]},
    #     ]
    # }
    # data_d = {
    #     'key_a': {'v_a1': None, 'v_a2': 2, 'v_a3': {}, 'v_a4': [4]},
    #     'key_b': [
    #         {'v_b5': {'v_b55': ''}},
    #         {'v_b6': ['6', 7, 8]},
    #         {'v_b7': [{'v_b77': 777}, {'v_b77': '666'}, {'v_b77': 555}]},
    #     ]
    # }
    #
    # data_type_check(data_d, data_t)
    # data_type_check(data_d['key_a']['v_a3'], dict)
    # data_type_check(None, int)
    # data_type_check({}, int)
    # data_type_check('a', int)
    # data_type_check(['a', 22222], (str, str))
    # data_type_check([], (str, str))

