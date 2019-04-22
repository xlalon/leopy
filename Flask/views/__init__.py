# -*- coding: utf-8 -*-

from .homepage import homepage, homepage_urls
from .user import user, user_urls


bp_and_urls = (
    (homepage, homepage_urls),
    (user, user_urls),
)
