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
		#auth0_certificate = "step1 - get Auth0 Certificate".encode("utf-8");
		auth0_certificate = self.auth0_action.step1_get_auth0_certificate()
		#logger.debug(" auth0 certificate : \n--\n{}\n--\n".format(auth0_certificate))
		logger.debug(" auth0 certificate : \n--\n{}\n--\n".format(auth0_certificate['access_token']))

		##fake_token_dict = { 'roles': 'x, y, z', 'access_token':' token stuff here', 'footer':'jajahd '}
		##tenant_list = self.auth0_action.step2_get_auth0_tenants(auth0_certificate)
		tenant_list = self.auth0_action.retrieve_organizations(auth0_certificate)
		#logger.debug(" auth0 tenant list : %s".format(tenant_list))

		#logger.debug("step2 - get Auth0 tenants")
		#logger.debug("step3 - for each tenant, get userlist")
		#logger.debug("step4 - for each tenant-user, get role data")

		#new_loop = asyncio.new_event_loop()
		#t = Thread(target=self.start_loop, args=(new_loop,))
		#t.start()

		# it’s best to use their _threadsafe alternatives. Let’s see how that looks:

		#new_loop.call_soon_threadsafe(self.more_work, 6)

		'''
		        # What if instead of doing everything in the current thread, we spawn a separate Thread to do the work for us.
		        Notice that this time we created a new event loop through asyncio.new_event_loop(). The idea is to spawn a new thread, pass it that new loop and then call thread-safe functions (discussed later) to schedule work.

		        The advantage of this method is that work executed by the other event loop will not block execution in the current thread. Thereby allowing the main thread to manage the work, and enabling a new category of execution mechanisms.
		        '''
		new_loop = asyncio.new_event_loop()
		t = Thread(target=self.start_loop, args=(new_loop,))
		t.start()

		# it’s best to use their _threadsafe alternatives. Let’s see how that looks:

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


