# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from config.app_creation import create_app
from rpc.service.server import run as rpc_run


app = create_app()

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port=5555, use_debugger=True))


if __name__ == '__main__':
    # rpc serve
    rpc_run('127.0.0.1', 5556)
    manager.run()
