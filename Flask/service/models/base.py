# -*- coding: utf-8 -*-

from models import db


class BaseModelService:

    def __init__(self):
        self.db = db

    def model2_dict(self, model_ins, model_attrs=None, default=None):
        """数据库实例转换成字典"""
        if model_ins and isinstance(model_ins, self.db.Model):
            model_ins = {k: v for k, v in vars(model_ins).items() if not k.startswith('_')}
        else:
            model_ins = {}
        if model_attrs:
            if isinstance(model_attrs, str):
                model_attrs = [model_attrs]
            assert isinstance(model_attrs, (list, tuple))
            model_dict = {k: model_ins.get(k, default) for k in model_attrs}
        else:
            model_dict = model_ins
        return model_dict
