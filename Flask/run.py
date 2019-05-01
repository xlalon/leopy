# -*- coding: utf-8 -*-

from flask_script import Manager
from config.server_init.app_creation import create_app


app = create_app()

manager = Manager(app)


if __name__ == '__main__':
    manager.run()
