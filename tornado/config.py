# -*- coding: utf-8 -*-


class _CodeConfig:
    CODE_OK = '0'
    # 固定8位，前4位为常规的百位， 后4位为个位和十位
    # 比如`404` 为 0100（4）0100（04）
    CODE_PAGE_NOT_FOUND = '01000100'


class _DataBaseConfig:
    pass


class Config(_CodeConfig, _DataBaseConfig):
    pass
