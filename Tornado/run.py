# -*- coding: utf-8 -*-

import os
import sys
import tornado.ioloop
sys.path.append(os.path.abspath("."))

from app.routers import make_app


if __name__ == "__main__":
    app = make_app()
    app.listen(1024)
    tornado.ioloop.IOLoop.current().start()
