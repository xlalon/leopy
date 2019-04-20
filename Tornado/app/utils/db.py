# -*- coding: utf-8 -*-


def db_ins2dict(ins):
    """数据库模型转换成dict或者[dict, dict]"""
    data = None

    def _dbs_2dict(_ins):
        if _ins:
            _ins = vars(_ins)
            _ins.pop('_sa_instance_state', None)
            return _ins
    if isinstance(ins, list):
        data = [_dbs_2dict(i) for i in ins]
    elif ins:
        data = _dbs_2dict(ins)

    return data
