import asyncio
import time
from threading import Thread
import os

import logging
logger = logging.getLogger("RealplaySync")


class Auth0Controller:
	def __init__(self, param_logger):
		self.auth0_controller = 'auth0_controller'
		self.logger = param_logger

	def yes_you_can_log_from_here(self):
		logger.debug(" MY MY MY yes_you_can_log_from_here ")

	def show_log_levels_auth0(self):
		logger.critical("LogTest - Your program has done something awful")
		logger.error("LogTest - Something has gone very wrong")
		logger.warning("LogTest - You've been warned")
		logger.info("LogTest - Here's some info")
		logger.debug("LogTest - Debugging information")

	def ok_now_we_can_build_things(self):
		logger.debug("step1 - get Autho tenants")
		logger.debug("step2 - for each tenant, get userlist")
		logger.debug("step3 - for each tenant-user, get role data")