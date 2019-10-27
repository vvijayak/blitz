# -*- coding: utf-8 -*-
"""This module contains an empty application container.
It is defined here to avoid circular imports
"""
from mindmeld import Application
import logging
import os


def get_logger():
    logger = logging.getLogger('blitz')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

app = Application(__name__)
PATH = os.path.realpath(os.path.dirname(__file__))
NFL_DATA_PATH = f'{PATH}/nfl/data'
DEFAULT_TEAM = 'Seahawks'

__all__ = ['app']
