# -*- coding: utf-8 -*-

import sys

from utils.server_init import create_app


def read_mode_from_command():
    for var in sys.argv[1:]:
        mode_name, mode_type = var.split('=')
        if mode_name == 'mode':
            return mode_type
    return 'test'


if __name__ == '__main__':
    mode = read_mode_from_command()
    app = create_app(mode=mode)
    app.run()
