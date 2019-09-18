# -*- coding: utf-8 -*-
import os
from ast import literal_eval


def env_config(name, eval_=False):
    v = os.environ.get(name)
    if eval_:
        v = literal_eval(v)
    return v
