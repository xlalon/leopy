# -*- coding: utf-8 -*-

from .base import BaseTestCase
from app.utils.helpers import *

_OBJECT = object()


class HelperTestCase(BaseTestCase):

    def test_to_int(self):
        # int类型转换
        self.assertEqual(to_int(10), 10)
        self.assertEqual(to_int(-10), -10)
        self.assertEqual(to_int(10, base=8), 8)
        # float类型转换
        self.assertEqual(to_int(10.4), 10)
        self.assertEqual(to_int(-10.4), -10)
        self.assertEqual(to_int(10.4, base=8), 8)
        # 字符串整形转换
        self.assertEqual(to_int('10'), 10)
        self.assertEqual(to_int('-10'), -10)
        self.assertEqual(to_int('10', base=8), 8)
        # 字符串float转换
        self.assertEqual(to_int('10.4'), 10)
        self.assertEqual(to_int('-10.3'), -10)
        self.assertEqual(to_int('10.3', base=8), 8)
        # 不能转换时候返回default值
        self.assertEqual(to_int('abc123'), 0)
        self.assertEqual(to_int(None), 0)
        self.assertEqual(to_int([], dft=10), 10)
        # 不能转换时候引发异常
        self.assertRaises(ValueError, to_int, s='abc123', e_raise=True)
        self.assertRaises(ValueError, to_int, None, e_raise=True)
        self.assertRaises(ValueError, to_int, [], e_raise=True)

    def test_is_dict(self):
        data = {'key_a': {'key_b': {'key_c': ['value_1', 'value_2']}}}
        self.assertEqual(is_dict(data), True)
        # 单key
        self.assertEqual(is_dict(data, key_flow='key_a'), True)
        # key_flow
        self.assertEqual(is_dict(data, key_flow=['key_a', 'key_b']), True)
        # 跨key
        self.assertEqual(is_dict(data, 'key_b'), False)
        self.assertEqual(is_dict(data, ['key_a', 'key_c']), False)

    def test_dict_get(self):
        # 字典获取存在的key值
        data = {'key_a': {'key_b': ['value_1', 'value_2']}, 'key_b': 'value_b'}
        self.assertEqual(dict_get(data, 'key_a'), {'key_b': ['value_1', 'value_2']})
        self.assertEqual(dict_get(data, ['key_a', 'key_b']), ['value_1', 'value_2'])
        self.assertEqual(dict_get(data, ('key_a', 'key_b')), ['value_1', 'value_2'])
        # 字典获取不存在的key值
        self.assertEqual(dict_get({}, 'key_a', default='DEFAULT'), None)
        self.assertEqual(dict_get(data, 'key_c'), None)
        self.assertEqual(dict_get(data, ['key_a', 'key_b', 'key_c']), None)
        self.assertEqual(dict_get(data, ['key_b', 'key_c'], default='DEFAULT'), 'DEFAULT')
        # 非字典对象返回默认值
        self.assertEqual(dict_get(None, 'key_a', default='DEFAULT'), 'DEFAULT')
        self.assertEqual(dict_get([], ['key_a', 'key_b'], default='DEFAULT'), 'DEFAULT')
        self.assertEqual(dict_get(set(), ['key_a', 'key_b'], default='DEFAULT'), 'DEFAULT')
        self.assertEqual(dict_get('', 'key_a', default='DEFAULT'), 'DEFAULT')
        self.assertEqual(dict_get(123, ['key_a', 'key_b'], default='DEFAULT'), 'DEFAULT')
        self.assertEqual(dict_get(123.456, 'key_a', default='DEFAULT'), 'DEFAULT')
        self.assertEqual(dict_get('123.456', ['key_a', 'key_b'], default='DEFAULT'), 'DEFAULT')
        self.assertEqual(dict_get(_OBJECT, 'key_a', default='DEFAULT'), 'DEFAULT')

    def test_dict_up4_dict(self):
        dst = {'a': 1, 'b': 2}
        src = {'a': 10, 'c': {'d': 30}}
        # 不提供dst_keys更新src全部键值对到dst, 返回新字典
        self.assertEqual(dict_up4_dict(dst, src), {'a': 10, 'b': 2, 'c': {'d': 30}})
        # 只提供dst_keys, 只跟新对应键值
        self.assertEqual(dict_up4_dict(dst, src, dst_keys=['a']), {'a': 10, 'b': 2})
        # 提供dst_keys和src_keys, 更新src_keys key值到对应dst_keys key值
        self.assertEqual(dict_up4_dict(dst, src, dst_keys=['a'], src_keys=['c']), {'a': {'d': 30}, 'b': 2})
        # 只提供src_keys并只为dict, 更新dst，键名为src_keys中键， 值为src中以src_keys中值为键的值
        self.assertEqual(dict_up4_dict(dst, src, src_keys={'a': 'new_a'}), {'new_a': 10, 'b': 2})
        self.assertEqual(dict_up4_dict(dst, src, src_keys={'c': 'new_c'}), {'a': 1, 'b': 2, 'new_c': {'d': 30}})

    def test_str_cmp(self):
        # 等值比较
        self.assertEqual(str_cmp('a', 'a'), True)
        self.assertEqual(str_cmp('a', 'a', 'a'), True)
        # 非等值比较
        self.assertEqual(str_cmp('a', 'A'), False)
        self.assertEqual(str_cmp('a', 'a', 'A'), False)
        # 不等值比较
        self.assertEqual(str_cmp('a', 'A', eq=False), True)
        self.assertEqual(str_cmp('a', 'a', 'A', eq=False), True)
        # 忽略大小写
        self.assertEqual(str_cmp('a', 'A', ignore_case=True), True)
        self.assertEqual(str_cmp('a', 'a', 'A', ignore_case=True), True)
        self.assertEqual(str_cmp('a', 'A', eq=False, ignore_case=True), False)
        self.assertEqual(str_cmp('a', 'a', 'A', eq=False, ignore_case=True), False)
        # 非法比较
        self.assertRaises(ValueError, str_cmp, 'a')
        self.assertRaises(TypeError, str_cmp, *(1, 'a'))

    def test_drop_dict_items(self):
        data = {'a': 1, 'b': [2], 'c': '', 'd': 0, 'e': -1, 'f': [], 'g': None, 10: 12}
        # 单个key
        self.assertEqual(drop_dict_items(data, drop_key='a'),
                         {'b': [2], 'c': '', 'd': 0, 'e': -1, 'f': [], 'g': None, 10: 12})
        # 多个key
        self.assertEqual(drop_dict_items(data, drop_key=['a', 'b', 'c']),
                         {'d': 0, 'e': -1, 'f': [], 'g': None, 10: 12})
        # 单个value
        self.assertEqual(drop_dict_items(data, drop_value=''),
                         {'a': 1, 'b': [2], 'd': 0, 'e': -1, 'f': [], 'g': None, 10: 12})
        # 多个value
        self.assertEqual(drop_dict_items(data, drop_value=['', [], None, 12]),
                         {'a': 1, 'b': [2], 'd': 0, 'e': -1})
        # 单个key和value
        self.assertEqual(drop_dict_items(data, drop_key='a', drop_value=''),
                         {'b': [2], 'd': 0, 'e': -1, 'f': [], 'g': None, 10: 12})
        # 多个key和value
        self.assertEqual(drop_dict_items(data, drop_key=['a', 'b'], drop_value=['', None, [], 12]),
                         {'d': 0, 'e': -1})
        # 删除不存在的key和value
        self.assertEqual(drop_dict_items(data, drop_key='aa', drop_value='123456'),
                         {'a': 1, 'b': [2], 'c': '', 'd': 0, 'e': -1, 'f': [], 'g': None, 10: 12})
