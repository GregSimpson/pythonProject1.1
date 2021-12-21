import asyncio
import http
import json

# https://stackoverflow.com/questions/6198372/most-pythonic-way-to-provide-global-configuration-variables-in-config-py
# import api/src/globals() as gl
from ..schema.auth0_async import Auth0AsyncSchema
from ..route import globals as gl

import logging
logger = logging.getLogger("RealplaySync")

import http
import time
from threading import Thread

import mmap
import os


class ReportsModel:
    def __init__(self):
        self.reports_process = 'reports_process'
        logger.debug("{}".format(self.reports_process))
        logger.debug("ini client_id variable     : {}".format(gl.client.id))
        logger.debug("ini client_secret variable : {}".format(gl.client.secret))

    def report_errors(self):
        '''
            default_path='errors.log',
            num_of_lines=20,
            default_level=logging.DEBUG,
            env_key='LOG_CFG'
    ):'''

        my_reports_model = ReportsModel()
        #my_reports_model.tailer(default_path, default_path, num_of_lines)
        logger.info("finished report_errors")
        logger.debug("ERROR REPORT BEGIN")
        logger.debug(".")
        logger.debug(my_reports_model.tailer_errors())
        logger.debug(".")
        logger.debug("ERROR REPORT END")

        return(my_reports_model.tailer_errors())


    def report_info(self):
        '''
            default_path='errors.log',
            num_of_lines=20,
            default_level=logging.DEBUG,
            env_key='LOG_CFG'
    ):'''

        my_reports_model = ReportsModel()
        #my_reports_model.tailer(default_path, default_path, num_of_lines)
        logger.info("finished report_info")
        logger.debug("INFO REPORT BEGIN")
        logger.debug(".")
        logger.debug(my_reports_model.tailer_info()) #'info.log'))
        logger.debug(".")
        logger.debug("INFO REPORT END")

        return(my_reports_model.tailer_info())


    # https: // stackoverflow.com / questions / 136168 / get - last - n - lines - of - a - file - similar - to - tail / 136368  # 136368


    def tailer_errors(self):
        filename='errors.log'
        n=20
        """Returns last n lines from the filename. No exception handling"""
        size = os.path.getsize(filename)
        with open(filename, "rb") as f:
            # for Windows the mmap parameters are different
            fm = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
            try:
                for i in range(size - 1, -1, -1):
                    if fm[i] == '\n':
                        n -= 1
                        if n == -1:
                            break
                return fm[i + 1 if i else 0:].splitlines()
            finally:
                fm.close()

    def tailer_info(self):
        filename='info.log'
        n=20
        """Returns last n lines from the filename. No exception handling"""
        size = os.path.getsize(filename)
        with open(filename, "rb") as f:
            # for Windows the mmap parameters are different
            fm = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
            try:
                for i in range(size - 1, -1, -1):
                    if fm[i] == '\n':
                        n -= 1
                        if n == -1:
                            break
                return fm[i + 1 if i else 0:].splitlines()
            finally:
                fm.close()

