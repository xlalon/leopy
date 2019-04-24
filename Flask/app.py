# -*- coding: utf-8 -*-

import argparse

from utils.server_init import create_app


def read_mode_from_command():
    args = argparse.ArgumentParser()
    args.add_argument('--mode', nargs=1, type=str, default=['test'], help='Run mode')
    args = args.parse_args()
    run_mode = args.mode[0]

    return run_mode


if __name__ == '__main__':
    mode = read_mode_from_command()
    app = create_app(mode)
    app.run()
