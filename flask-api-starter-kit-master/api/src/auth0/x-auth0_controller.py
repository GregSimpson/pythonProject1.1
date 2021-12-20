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
		logger.debug(" yes_you_can_log_from_here ")

	def show_log_levels_auth0(self, protocol="https"):
		self.setup_logging()
		logger.critical("LogTest - Your program has done something awful")
		logger.error("LogTest - Something has gone very wrong")
		logger.warning("LogTest - You've been warned")
		logger.info("LogTest - Here's some info")
		logger.debug("LogTest - Debugging information")

	# -----
	import os
	import logging.config
	import yaml
#	logger = logging.getLogger("RealplaySync")

	def setup_logging(
			default_path='logging.yaml',
			default_level=logging.DEBUG,
			env_key='LOG_CFG'
	):
		"""Setup logging configuration

		"""
		path = default_path
		value = os.getenv(env_key, None)
		if value:
			path = value
		if os.path.exists(path):
			with open(path, 'rt') as f:
				config = yaml.safe_load(f.read())
			logging.config.dictConfig(config)
		else:
			logging.basicConfig(level=default_level)

# -----
