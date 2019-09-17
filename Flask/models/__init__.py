# -*- coding: utf-8 -*-

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def to_dict(db_obj):
    data = {}
    if isinstance(db_obj, db.Model):
        for column, value in vars(db_obj).items():
            if column.startswith('_'):
                continue
            if isinstance(value, (datetime, date)):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            data[column] = value
    return data


db.Model.to_dict = to_dict
