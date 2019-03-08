# -*- coding: utf-8 -*-

import ast
import copy
import os.path
import re
from datetime import datetime
from pytz import timezone

import config
from pprint import pprint


def req_get(instance, need_args):
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
    except AttributeError:
        return False
    else:
        return isinstance(data, dict)


def dict_get(data, key_flow, *, default=None):
    """
    从原始dict中获取指定深度key的值
    :param data: 原始数据
    :param key_flow: 想要获取数据的依次序的key
    :param default: 没有获取到值返回默认值
    [In]:  dict_get(None, 'a', default='123')
    [Out]: '123'
    [In]:  data = {'a': {'b': {'c': {'d': 1}}}}
    [In]:  dict_get(data, key_flow=['a', 'b', 'c', 'd'])
    [Out]: 1
    """
    if isinstance(key_flow, str):
        key_flow = [key_flow]
    try:
        for key in key_flow:
            data = data.get(key, default)
    except AttributeError:
        return default
    else:
        return data


def drop_dict_items(data, *, drop_key=None, drop_value=float('inf')):
    """
    返回一个过滤字典中不需要的键值对（KEY或者VALUE）的新字典结构
    注意： 默认会删除值为float('inf')的键值对, 这个值基本不用
    :param data: 待过滤的字典
    :param drop_key: 指定需要删除的key的键值对, 可以为单个key, 也可以为一个list, tuple, set, dict(只删除相同键)
    :param drop_value: 指定需要删除的value的键值对
    [In]:  a = {'a': 1, 'b': [2], 'c': '', 'd': 0, 'e': -1, 'f': [], 'g': None, 10: 12}
    [In]:  drop_dict_items(a, drop_key='a', drop_value='')
    [Out]:  {'b': [2], 'd': 0, 'e': -1, 'f': [], 'g': None, 10: 12}
    [In]:  drop_dict_items(a, drop_key=['a', 'b'], drop_value=['', None, [], 12])
    [Out]: {'d': 0, 'e': -1}
    """
    if not isinstance(data, dict):
        raise TypeError("drop_dict_items arg data only support dict type, got {}".format(type(data).__name__))
    if drop_value in [None, [], {}, set(), tuple()] or isinstance(drop_value, (str, int, float)):
        drop_value = [drop_value]
    # 元组特殊，要小心
    if not isinstance(drop_key, (list, tuple, set, dict)):
        drop_key = [drop_key]
    # 过滤值为指定value的键值对
    return dict((k, v) for k, v in data.items() if v not in drop_value if k not in drop_key)


def to_int(s, dft=0, e_raise=False, base=10):
    """对象转换成整型，对于不能转换的返回dft
    :param s:    需要转换的对象
    :param base: 进制，默认是10进制
    :param dft:  对象不能转换成整形默认返回值
    :param e_raise: 当不可转换为整形时， 该函数是否抛出异常， 默认不抛出异常，并返回dft值
    [In]:  to_int('10.0')
    [Out]: 10
    [In]:  to_int('asd', dft=10)
    [Out]: 10
    [In]:  to_int(None, e_raise=True)
    [Out]: ValueError: to_int cannot trans `None` to int
    """
    try:
        return int(str(int(float(str(s)))), base=base)
    except ValueError:
        if e_raise is True:
            raise ValueError("to_int cannot trans `{}` to int".format(s))
        return dft


def str_cmp(*str_s, eq=True, ignore_case=False):
    """
    :param str_s: 待比较的字符串
    :param eq: True/False 返回待比较的字符串是否相等
    :param ignore_case: True/False 待比较的字符串是否忽悠大小写
    :return: True/False
    [In]:  str_cmp('a', 'A')
    [Out]: False
    [In]:  str_cmp('a', 'A', ignore_case=True)
    [Out]: True
    [In]:  str_cmp('a', 'A', eq=False)
    [Out]: True
    [In]:  str_cmp('a', 'a', 'A', ignore_case=True)
    [Out]: True
    """
    if len(str_s) < 2:
        raise ValueError('str_cmp need at least two strings to compare')
    if not all(isinstance(str_, str) for str_ in str_s):
        raise TypeError('str_cmp only support str type to compare')
    if ignore_case is True:
        str_s = (str_.lower() for str_ in str_s)
    if eq is False:
        return len(set(str_s)) >= 2
    return len(set(str_s)) == 1


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


def dict_up4_dict(dst, src, dst_keys=None, src_keys=None, default=None):
    """从src中更新到dst，返回一个`新的字典`(不影响原来的数据)
    :param dst          需要更新的字典
    :param src          源字典
    :param dst_keys     dst需要更新的key（列表/元组）
    :param src_keys     src中的key（列表/元组）
    :param default      无存在值返回的默认值
    若不提供dst_keys, 且不提供src_keys, 默认更新src全部键值对到dst
    src_keys为list/tuple时, dst_keys和src_keys更新的键名称一一对应
    src_keys 为dict时, 键名称从src_keys键更新成src_keys值
    """
    result = copy.deepcopy(dst)
    if dst_keys is None:
        dst_keys = src.keys()
    if src_keys is None:
        result.update((k, src.get(k, default)) for k in dst_keys)
    else:
        if isinstance(src_keys, (list, tuple)):
            result.update((k, src.get(src_k, default)) for k, src_k in zip(dst_keys, src_keys))
        # src_keys为dict时, 更换指定key名称, key，value为更换前/后的键名
        elif isinstance(src_keys, dict):
            for old_k, new_k in src_keys.items():
                result[new_k] = src.get(old_k, default)
                result.pop(old_k, None)
    return result


def dict2_hds(src):
    if isinstance(src, dict):
        for k, v in src.items():
            print('{}: {}'.format(k, v))


class ObjectDict(dict):
    def __init__(self, data, *args, **kwargs):
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    kwargs[k] = ObjectDict(v)
                else:
                    kwargs[k] = v
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def str2_ts(dt_str, dt_fmt='%Y-%m-%d %H:%M:%S', tz=None):
    """字符串时间转换成时间戳，默认提供字符串的格式为：日期 时间(2018-12-28 12:24:36)，
    如果字符串只有日期部分，但是格式为%Y-%m-%d则不用另外提供信息，其他格式则提供格式dt_fmt, 如'%Y-%d-%m %H:%M'。
    默认字符串时间是本地时间，可指定字符串的时区信息， tz如 'UTC', 'Etc/GMT-7'
    """
    dt_tuple = datetime.strptime(dt_str, dt_fmt).timetuple()[:6]
    dt = datetime(*dt_tuple, tzinfo=timezone(tz)) if tz else datetime(*dt_tuple)
    return int(dt.timestamp())


def ts2_str(ts, fmt='%Y-%m-%d %H:%M:%S', tz=None):
    """时间戳转换成字符串, 默认转换格式为: 日期 时间(2018-12-28 12:24:36)。
     如果只需要日期，可以fmt='date', 如果只需要时间，可以fmt='time', 也可以自定义转换格式。
     默认转换成本地时间，可转换成指定时区时间。 tz如 'UTC', 'Etc/GMT-7'
    """
    fmt = {'date': '%Y-%m-%d', 'time': '%H:%M:%S'}.get(fmt, fmt)
    ts_tz = (float(ts), timezone(tz)) if tz else (float(ts),)
    return datetime.fromtimestamp(*ts_tz).strftime(fmt)


def analysis_aa():
    filename = os.path.join(config.Config.PROJECT_PATH, 'app/aa.txt')
    with open(filename, 'rb') as aa:
        aa_txt = aa.read().decode()
        aa_txt = re.split('=>', aa_txt, maxsplit=1)[1]
        aa_txt = aa_txt.replace('[', '{').replace(']', '}').replace(' ', '')
        aa_txt = aa_txt.replace('=>array(', ': {').replace(')', '}')
        aa_txt = aa_txt.replace('=>', ': ')
        aa_txt = aa_txt.replace('\n', '').replace('\t', '')
        aa_txt = ast.literal_eval(aa_txt)[0]
        aa_txt_r = {k: v for k, v in aa_txt.items() if k.startswith('ios') or k.startswith('and')}
        pprint(aa_txt_r)


def analysis_cart():
    import csv
    import re
    filename = os.path.join(config.Config.PROJECT_PATH, 'app/cart_info_error.csv')
    filename1 = os.path.join(config.Config.PROJECT_PATH, 'app/cart_info_error_memberIds.csv')

    ids_s = set()
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            id_s = re.findall('memberId=(.*?);', row[1])
            ids_s.add(id_s[0] if id_s and id_s[0].isdigit() else '')

    ids_s.remove('')

    with open(filename1, 'w') as f1:
        f1.write('MemberIds\n')
        for id_ in ids_s:
            f1.write(id_ + '\n')


if __name__ == '__main__':
    analysis_cart()
