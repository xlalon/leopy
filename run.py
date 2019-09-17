# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from config.app_creation import create_app


app = create_app()

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port=5555, use_debugger=True))


if __name__ == '__main__':
    manager.run()
