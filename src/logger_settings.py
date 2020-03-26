# -*- coding: utf-8 -*-
import logging


def logging_setup(logger_name=None, file_name='log.txt'):
    log = logging.getLogger(logger_name)
    log.setLevel(level=logging.INFO)
    handler = logging.FileHandler(file_name, 'a', 'utf-8')
    format = logging.Formatter('[%(asctime)s]-[Status:%(levelname)s]\n[start_msg]\n%(message)s\n[end_msg]\n\n')
    handler.setFormatter(format)
    log.addHandler(handler)

    return log