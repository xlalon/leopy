# -*- coding: utf-8 -*-

from .views.home import urls_home
from .views.user import urls_user

app_name = 'web'
urlpatterns = urls_home + urls_user
