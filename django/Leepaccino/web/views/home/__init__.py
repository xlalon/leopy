# -*- coding: utf-8 -*-

from django.urls import path
from .homepage import HomeView


urls_home = [
    path('', HomeView.as_view(), name='home'),
]
