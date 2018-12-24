# -*- coding: utf-8 -*-


def request_item_get(instance, need_args):
    """
    [In]:  request_kwargs(self, need_args=('token', 'uid'))
    [Out]: {'token': '171542133783_5bcd34f6561443.97165732_95f2603f0b9cf82a748cd599d55be3a214a1742b', 'uid': 0}
    """
    # 请求全部属性
    request_ = {attr_name: getattr(instance, attr_name) for attr_name in dir(instance)}
    # 初始化需要的属性字段
    result = {need_arg: '' for need_arg in need_args}
    # 忽略大小写
    need_args_lower = (arg.lower() for arg in need_args)
    for attr_name, attr_value in request_.items():
        # 忽略属性开始下划线
        if isinstance(attr_name, str) and attr_name.startswith('_'):
            attr_name = attr_name[1:]
        attr_name = attr_name.lower()
        if attr_name in need_args_lower:
            result[attr_name] = attr_value
    return result


def is_dict(data: dict, key_flow: [str, list, tuple] = None) -> bool:
    """
    检验数据是否是dict类型
    :param data: 待检测的原始数据
    :param key_flow: key依次深度的列表/元组, 也可以为单个字符串（只检查data[字符串]是否为dict
    [In]:  is_dict([])
    [Out]: False
    [In]:  data = {'a': {'b': {'c': {'d': 1}}}}
    [In]:  is_dict(data, 'a')
    [Out]: True
    [In]:  is_dict(data, key_flow=['a', 'b', 'c'])
    [Out]: True
    [In]:  is_dict(data, key_flow=['a', 'c'])
    [Out]: False
    """
    if not key_flow:
        return isinstance(data, dict)
    if isinstance(key_flow, str):
        key_flow = [key_flow]
    try:
        for key in key_flow:
            data = data.get(key)
    except (TypeError, AttributeError):
        return False
    else:
        return isinstance(data, dict)


def dict_get(data, key_flow, *, default=None):
    """
    从原始dict中获取指定深度key的值
    :param data: 原始数据
    :param key_flow: 想要获取数据的依次序的key
    :param default: 没有获取到值返回默认值
    [In]:  dict_get([], 'a')                   # 应用于南京返回的data结构不是dict(code不为0的时候)
    [Out]: None
    [In]:  dict_get(None, 'a', default='123')
    [Out]: '123'
    [In]:  data = {'a': {'b': {'c': {'d': 1}}}}
    [In]:  dict_get(data, key_flow='a')
    [Out]: {'b': {'c': {'d': 1}}}
    [In]:  dict_get(data, key_flow=['a', 'b', 'c', 'd'])
    [Out]: 1
    [In]:  dict_get(data, key_flow=['a', 'c', 'd'],  default='123')
    [Out]: '123'
    """
    if isinstance(key_flow, str):
        key_flow = [key_flow]
    try:
        for key in key_flow:
            data = data.get(key)
    except AttributeError:
        return default
    else:
        return data


def drop_invalid_dict_items(data, *, drop_key=None, drop_value=float('inf')):
    """
    返回一个过滤字典中不需要的键值对（KEY或者VALUE）的新字典结构
    注意： 默认会删除值为float('inf')的键值对, 这个值基本不用
    :param data: 待过滤的字典
    :param drop_key: 指定需要删除的key的键值对, 可以为单个key, 也可以为一个list, tuple, set, dict(只删除相同键)
    :param drop_value: 指定需要删除的value的键值对
    [In]:  a = {'a': 1, 'b': [2], 'c': '', 'd': 0, 'e': -1, 'f': [], 'g': None, 10: 12}
    [In]:  drop_invalid_dict_items(a, drop_key='a', drop_value='')
    [Out]:  {'b': [2], 'd': 0, 'e': -1, 'f': [], 'g': None, 10: 12}
    [In]:  drop_invalid_dict_items(a, drop_key=['a', 'b'], drop_value=['', None, [], 12])
    [Out]: {'d': 0, 'e': -1}
    """
    if not isinstance(data, dict):
        raise TypeError("drop_invalid_dict_items arguments data"
                        " only support dict type, got {}".format(type(data).__name__))
    if drop_value in ['', None, 0, [], {}, set(), tuple(), float('inf')] or isinstance(drop_value, (str, int, float)):
        drop_value = [drop_value]
    # 过滤值为指定value的键值对
    data = {k: v for k, v in data.items() if v not in drop_value}
    # 删除指定key键值对
    if drop_key:
        if not isinstance(drop_key, (list, tuple, set, dict)):
            drop_key = [drop_key]
        for k in drop_key:
            # 加入返回默认值是为了pop不报KeyError
            data.pop(k, None)
    return data


def to_int(s, default=0, invalid_s_raise=False, base=10):
    """
    字符串转换成整型，对于不能转换的返回default指定的数据
    :param s: 需要转换的字符串
    :param base: 多少进制，默认是10进制。如果是16进制，可以写0x或者0X
    :param default: 字符串不能转换成整形默认返回值
    :param invalid_s_raise: 不可转换时， 该函数是否抛出异常
    [In]:  to_int('10')
    [Out]: 10
    [In]:  to_int('asd')
    [Out]: 0
    [In]:  to_int('asd', invalid_s_raise=True)
    [Out]: ValueError: to_int argument 'asd' cannot trans to int
    """
    if isinstance(s, str) and s.isdigit():
        return int(s, base=base)
    else:
        # 添加 invalid_s_raise为了兼容以前的功能（报错直接返回 0）
        if invalid_s_raise:
            raise ValueError("to_int argument '{}' cannot trans to int".format(s))
        return default


def str_compare(*str_s, eq=True, ignore_case=False):
    """
    :param str_s: 待比较的字符串
    :param eq: True/False 返回待比较的字符串是否相等
    :param ignore_case: True/False 待比较的字符串是否忽悠大小写
    :return: True/False
    [In]:  str_compare('a', 'A')
    [Out]: False
    [In]:  str_compare('a', 'A', ignore_case=True)
    [Out]: True
    [In]:  str_compare('a', 'A', eq=False)
    [Out]: True
    [In]:  str_compare('a', 'a', 'A', ignore_case=True)
    [Out]: True
    """
    if len(str_s) < 2:
        raise ValueError('str_compare need at least two strings to compare')
    if not all(isinstance(str_, str) for str_ in str_s):
        raise TypeError('str_compare only support str type to compare')
    if ignore_case is True:
        str_s = (str_.lower() for str_ in str_s)
    if eq is False:
        return len(set(str_s)) >= 2
    return len(set(str_s)) == 1


def item_filter(dst, src):
    """
    数据过滤, 并返回 dst
    :param dst    目的数据(dict/[dict])
    :param src     源数据  (dict/[dict, dict, dict])
    当目的数据最外层为字典时， 源数据最外层必须为一个字典
    当目的数据最外层为列表时， 源数据最外层必须为一个列表
    若源数据中存在目的数据中键的值，则获取此值，若不存在或者不为真，则取原来的值
    [In]:  a = {'a': [{'b': ''}], 'c': '', 'd': 'D'}
    [In]:  b = {'a': [{'b': 'BB'}, {'b': 'BBB'}], 'c': 'CC'}
    [In]:  item_filter(a, b)
    [In]:  print(a)
    [Out]: {'a': [{'b': 'BB'}, {'b': 'BBB'}], 'c': 'CC', 'd': 'D'}
    [In]:  c =[{'a': [{'b': '', 'c': 'C'}]}]
    [In]:  d = [{'a': [{'b': 'BB'}]}, {'a': [{'b': 'BBB'}]}]
    [In]:  print(c)
    [In]:  item_filter(c, d)
    [Out]: [{'a': [{'b': 'BB', 'c': 'C'}]}, {'a': [{'b': 'BBB', 'c': 'C'}]}]
    """
    assert type(dst) == type(src), 'item_filter args must be the same type, got {} and {}'.format(
        type(dst).__name__, type(src).__name__)

    if isinstance(dst, list) and isinstance(src, list):
        src_len = len(src)
        dst.extend([{k: v for k, v in dst[0].items()} for _ in range(src_len-1)])
        for i in range(src_len):
            item_filter(dst[i], src[i])
        return

    for key, value in dst.items():
        if not isinstance(value, (dict, list)) and isinstance(src, dict):
            dst[key] = src.get(key, value) or value
        elif isinstance(value, dict) and isinstance(src, dict):
            item_filter(value, src.get(key))
        elif isinstance(value, list) and isinstance(src.get(key), list):
            src_len = len(src.get(key))
            dst[key] = [{k: v for k, v in value[0].items()} for _ in range(src_len)]
            for i in range(src_len):
                item_filter(dst[key][i], src.get(key)[i])


def items_filter(dst, src):
    """
    数据过滤 返回一个过滤后的数据
    :param dst  过滤规则(dict/[dict])
    :param src  源数据  (dict/[dict, dict])
    dst和src必须为同一数据类型(list(里面是字典)/dict)或者dst为字典src为列表
    若源数据中存在目的数据中需要的值，则取此值，若不存在或者不为真，则取原来的值
    [In]:  a = {'a': [{'b': ''}], 'c': '', 'd': 'D'}                           dst为字典
    [In]:  b = {'a': [{'b': 'BB'}, {'b': 'BBB'}], 'c': 'CC'}                   src为字典
    [In]:  items_filter(a, b)                                                  调用函数
    [Out]: {'a': [{'b': 'BB'}, {'b': 'BBB'}], 'c': 'CC', 'd': 'D'}             结果
    [In]:  c =[{'a': [{'b': '', 'c': 'C'}]}]                                   dst为列表
    [In]:  d = [{'a': [{'b': 'BB'}]}, {'a': [{'b': 'BBB'}]}]                   src为列表
    [In]:  items_filter(c, d)                                                  调用函数
    [Out]: [{'a': [{'b': 'BB', 'c': 'C'}]}, {'a': [{'b': 'BBB', 'c': 'C'}]}]   结果
    [In]:  e = {'a': [{'b': '', 'c': 'C'}]}                                    dst为字典
    [In]:  f = [{'a': [{'b': 'BB'}]}, {'a': [{'b': 'BBB'}]}]                   src为列表
    [In]:  items_filter(e, f)                                                  调用函数
    [Out]: [{'a': [{'b': 'BB', 'c': 'C'}]}, {'a': [{'b': 'BBB', 'c': 'C'}]}]   结果
    """
    def _filter(_dst, _src):
        result = {}
        for key, dft_v in _dst.items():
            value = _src.get(key)
            if isinstance(dft_v, dict) and isinstance(value, dict):
                result[key] = _filter(dft_v, value)
            elif dft_v and isinstance(dft_v, list) and isinstance(value, list) and isinstance(dft_v[0], dict):
                result[key] = [_filter(dft_v[0], info) for info in value]
            else:
                result[key] = value or dft_v
        return result
    # dst和src同为列表， 取dst[0](应该为一个字典)为过滤规则，对src里的每一个字典过滤
    if isinstance(src, list) and isinstance(dst, list):
        return [_filter(dst[0], info) for info in src]
    # dst和src同为字典， 取dst为过滤规则， 对src过滤
    elif isinstance(src, dict) and isinstance(dst, dict):
        return _filter(dst, src)
    # dst为字典, src为列表， 取dst为过滤规则, 对src里的每一个字典过滤
    elif isinstance(src, list) and isinstance(dst, dict):
        return [_filter(dst, info) for info in src]
    else:
        raise TypeError('items_filter args type invalid, got {} and {}'.format(
            type(dst).__name__, type(src).__name__))


def extract_dict_field(field_keys, src, default=''):
    """
    根据field_keys过滤字典src,返回一个新的字典对象
    :param field_keys 过滤key，可为list, tuple, set, dict
    :param src        数据源，为字典
    :param default    src中无field_keys中的key时默认值
    :return           字典对象
    """
    if not (isinstance(field_keys, (list, tuple, set, dict)) and isinstance(src, dict)):
        raise TypeError('extract_dict_field args type not right')
    return {key: src.get(key, default) for key in field_keys}


def dict2_pm_headers(src):
    if isinstance(src, dict):
        for k, v in src.items():
            print('{}: {}'.format(k, v))


class DataTree(dict):
    def __init__(self, data, *args, **kwargs):
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    kwargs[k] = DataTree(v)
                else:
                    kwargs[k] = v
        super().__init__(*args, **kwargs)
        self.__dict__ = self


if __name__ == '__main__':
    pass
    # a = {
    #     'code': '0',
    #     'msg': 'OK',
    #     'data':
    #         {'result': {
    #             'hello': [1, 2, 3]
    #         }}}
    # dt = DataTree(data=a)
    # print('code:', dt.code, 'data:', dt.data)
    # print(dt.data.result.hello)
