# -*- coding: utf-8 -*-

from app.services.test.hello_world import HelloWorldService


class BaseBusiness:

    def __init__(self):
        self.hello_world_svs = HelloWorldService()
