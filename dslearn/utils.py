# -*- coding:utf-8 -*-
__author__ = 'yajun'
import logging
from flask import flash

def flasher(msg, severity=None):
    """Flask's flash if available, logging call if not"""
    try:
        flash(msg, severity)
    except RuntimeError:
        if severity == 'danger':
            logging.error(msg)
        else:
            logging.info(msg)
