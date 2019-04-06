# -*- coding: utf-8 -*-


def service_off_model_info():
    """模特信息"""
    return {'model': ''}


def service_off_comments_overview():
    """评论概览"""
    return {"commentInfo": {}}


def service_off_sku_goods():
    """推荐商品"""
    return {"products": []}


def service_off_is_save():
    """"用户是否收藏该商品"""
    return {"result": 0}


def service_off_fault_tolerant():
    """容错推荐"""
    return '0', {'goods': []}
