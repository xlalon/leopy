# -*- coding: utf-8 -*-

from django.db import models
from time import time


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=64, null=False)
    token = models.CharField(max_length=128, null=False)
    username = models.CharField(max_length=32, null=False)
    realname = models.CharField(max_length=128, null=True, default='')
    birthday = models.CharField(max_length=10)
    join_time = models.CharField(max_length=10)
    update_time = models.CharField(max_length=10, default=str(int(time())))

    class Meta:
        db_table = 'user'
