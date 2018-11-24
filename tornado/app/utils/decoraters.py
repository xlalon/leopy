# -*- coding: utf-8 -*-

import inspect
from functools import partial, wraps
from .helpers import dict_get, is_dict

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
    :param switch
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


# def data_monitor(func=None, default=None, switch=SWITCH):
#     """数据开关
#     :param func
#     :param default
#     :param switch
#     """
#     # 参数可选支持
#     if func is None:
#         return partial(data_monitor, default=default, switch=switch)
#
#     @wraps(func)
#     async def _(*args, **kwargs):
#         if switch is False:
#             try:
#                 data = await func(*args, **kwargs)
#             except (HTTPError, RequestHttpError):
#                 return default() if callable(default) else default
#             else:
#                 return data
#     return _


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


# async def set_goods_price(header_dict, products, goods_id_keys='goods_id'):
#     """更新商品的实时价格
#     :param header_dict    头信息
#     :param products       商品列表, 形如[{商品信息},{商品信息},{商品信息}]
#     :param goods_id_keys  商品id在商品信息里的嵌套key
#     :return               只是更新products,不返回任何东西
#     在app.common.decorate.set_goods_price里有此函数的装饰器
#     """
#     goods_id_lst = [dict_get(product, goods_id_keys) for product in products]
#     # _, data = await RealTimePricesOrSizesService().get_real_time_prices(
#     #     header_dict=header_dict, goods_id_lst=goods_id_lst)
#     data = {'products': [{'goods_id': '12345'}]}
#     # 若不存在价格信息，则放弃更新
#     if not (is_dict(data, 'prices') and dict_get(data, 'prices')):
#         return
#     price_data = data['prices']
#     for product in products:
#         if not isinstance(product, dict):
#             continue
#         goods_id = str(dict_get(product, goods_id_keys))
#         if goods_id in price_data:
#             # 假定商品id和商品价格信息处在同一级别, 若商品id和价格信息信息处在更深嵌套, 则进入相应的商品信息
#             if isinstance(goods_id_keys, list):
#                 product_key = goods_id_keys[:-1]
#                 if product_key:
#                     product = dict_get(product, product_key)
#             product.update(price_data[goods_id])
#
#
# def set_goods_price_wrap(func=None, products_keys='products', goods_id_keys='goods_id'):
#     """实时更新商品价格装饰器
#     1. 被装饰的函数里面必须有header_dict这个位置参数
#     2. 被装饰的函数返回的信息可以为: data/code, data/code, data, msg，
#        其中I. data数据为dict, 此种数据结构必须指定一个嵌套的products_keys为商品列表，不提供默认为'products',
#               单个key可以为字符串， 嵌套key则提供列表，列表内依次为嵌套key
#               如： products_keys='products'则商品列表为data['products']
#                    products_keys=['whishlist','goods']则商品列表为data['whishlist']['goods']
#               商品列表里为商品信息，应该是[{商品信息}, {商品信息}, {商品信息}]这种形式
#               如[{'goods_id': '12345', 'goods_sn': 'abc', retailPrice: {...}, ...}, {商品信息}, {商品信息}]
#           II. data数据为list, 如[{'goods_id': '12345', 'goods_sn': 'abc', retailPrice: {...}, ...}, {商品信息}]
#     3. 此函数假定商品信息里的价格信息和商品id同处一个级别, 而可以通过goods_id_keys嵌套key获取到商品id
#        若不提供goods_id_keys信息默认为当前层的goods_id
#        如{'goodsId': {'goods_id': '123', 'retailPrice': {...}}}则goods_id_keys应该为['goodsId', 'goods_id']
#     此装饰器只更新商品价格部分，其他返回值不改变
#     """
#     if func is None:
#         return partial(set_goods_price_wrap, products_keys=products_keys, goods_id_keys=goods_id_keys)
#
#     @wraps(func)
#     async def _(*args, **kwargs):
#         header_dict = kwargs.get('header_dict')
#         data = await func(*args, **kwargs)
#         info = None
#         if len(data) == 1:
#             info = data
#         elif len(data) == 2:
#             _, info = data
#         elif len(data) == 3:
#             _, info, _ = data
#         if isinstance(info, dict):
#             products = dict_get(info, products_keys, default=[])
#             if isinstance(products, list):
#                 await set_goods_price(header_dict, products, goods_id_keys)
#         elif isinstance(info, list):
#             await set_goods_price(header_dict, info, goods_id_keys)
#         return data
#     return _


@type_assert(int, c=str)
def test_type_assert(a, b, c):
    print(a, b, c)


if __name__ == '__main__':
    test_type_assert(1, 2, 'a')
    test_type_assert(1, 2, 3)
