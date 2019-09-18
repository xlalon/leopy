# -*- coding: utf-8 -*-

import os
import logging

from config import BASE_DIR


def get_logger(name, stream_level=logging.INFO, file_level=logging.INFO):
    name = str(name)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not name.endswith('.log'):
        name += '.log'
    logger_filepath = os.path.join(BASE_DIR, 'logs', name)
    fh = logging.FileHandler(logger_filepath)
    fh.setLevel(file_level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(stream_level)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
