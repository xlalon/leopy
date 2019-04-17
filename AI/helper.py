# -*- coding: utf-8 -*-

__all__ = ['dict2_hds']


def dict2_hds(src):
    if isinstance(src, dict):
        for k, v in src.items():
            print('{}: {}'.format(k, v))


if __name__ == '__main__':
    print('Hello, Beautiful!')
