import asyncio
import time
from threading import Thread
import os

#from auth0_actions import Auth0Actions
#import auth0_actions
from ..src import auth0_actions as possible_actions

import logging
logger = logging.getLogger("RealplaySync")


class Auth0Controller:
	def __init__(self, param_logger):
		self.auth0_controller = 'auth0_controller'
		self.logger = param_logger
		self.auth0_action = possible_actions.Auth0Actions()

	def yes_you_can_log_from_here(self):
		logger.debug(" MY MY MY yes_you_can_log_from_here ")

	def show_log_levels_auth0(self):
		logger.critical("LogTest - Your program has done something awful")
		logger.error("LogTest - Something has gone very wrong")
		logger.warning("LogTest - You've been warned")
		logger.info("LogTest - Here's some info")
		logger.debug("LogTest - Debugging information")

	def ok_now_we_can_build_things(self):
		logger.debug("step1 - get Auth0 Certificate")
		auth0_certificate = self.auth0_action.step1_get_auth0_certificate()
		#logger.debug(" auth0 certificate : \n--\n{}\n--\n".format(auth0_certificate['access_token']))


		##tenant_list = self.auth0_action.retrieve_organizations(auth0_certificate)
		##logger.debug(" auth0 tenant list : {}".format(tenant_list))


		# https://github.com/auth0/auth0-python#management-sdk
		#logger.debug("github_example : {}".format("BEGIN"))
		#github_results = self.auth0_action.github_example(auth0_certificate)
		#logger.debug("github_example : {}".format("END"))
		#logger.debug("github_example results : {}\n\n".format(github_results))

		# hardcoded userid works!!!
		logger.debug("Retrieve Orgs : {}".format("BEGIN"))
		export_job = self.auth0_action.retrieve_userdata(auth0_certificate)
		logger.debug("Retrieve Orgs : {}".format("END"))
		logger.debug(" Retrieve Orgs results : {}".format(export_job))


		logger.debug("Exporting Job : {}".format("BEGIN"))
		#export_job = self.auth0_action.export_userlist(auth0_certificate)
		export_job = self.auth0_action.gjs_example(auth0_certificate)
		logger.debug("Exporting Job : {}".format("END"))
		logger.debug(" export job results : {}\n\n".format(export_job))

		#time.sleep(15)
		#logger.debug("Retrieve Orgs : {}".format("BEGIN"))
		#export_job = self.auth0_action.retrieve_organizations(auth0_certificate)
		#logger.debug("Retrieve Orgs : {}".format("END"))
		#logger.debug(" Retrieve Orgs results : {}".format(export_job))


		#logger.debug("step2 - get Auth0 tenants")
		#logger.debug("step3 - for each tenant, get userlist")
		#logger.debug("step4 - for each tenant-user, get role data")

		logger.debug(" FINISHED")

		#new_loop = asyncio.new_event_loop()
		#t = Thread(target=self.start_loop, args=(new_loop,))
		#t.start()

		# it’s best to use their _threadsafe alternatives. Let’s see how that looks:
		new_loop = asyncio.new_event_loop()
		t = Thread(target=self.start_loop, args=(new_loop,))
		t.start()
		new_loop.call_soon_threadsafe(self.more_work, 6)
		new_loop.call_soon_threadsafe(self.more_work, 3)


	async def do_some_work(x):
		logger.debug("Waiting {}".format(str(x)))
		await asyncio.sleep(x)

	def more_work(self, x):
		#logger.debug("starting {}".format(str(x)))
		time.sleep(x)
		#logger.debug("finished {}".format(str(x)))

	def start_loop(self, loop):
		try:
			asyncio.set_event_loop(loop)
			loop.run_forever()
		finally:
			loop.close()


