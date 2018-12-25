# -*- coding: utf-8 -*-

from .base import BaseTestCase


class HelperTestCase(BaseTestCase):

    def test_to_int(self):
        from app.utils.helpers import to_int
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
