#! /usr/env/python
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

from utils.helper import env_config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

load_dotenv(os.path.join(BASE_DIR, '.env'))

DEBUG = env_config('DEBUG', eval_=True)

if DEBUG:
    from config.settings.setting_dev import DevDeConfig
    Config = DevDeConfig
else:
    from config.settings.setting_pro import ProDeConfig
    Config = ProDeConfig
