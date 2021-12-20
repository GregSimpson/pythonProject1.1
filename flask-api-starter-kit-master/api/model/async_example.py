import asyncio
import time
from threading import Thread

from ..src import auth0_controller as a0

import logging
logger = logging.getLogger("RealplaySync")

class AsyncExampleModel:
    def __init__(self):
        self.async_example = 'async_example'

        ###setup_logging()
        #### #logger = logging.getLogger("RealplaySync")

        #print("\n\t\tgjs >>> {}".format(self.async_example))
        logger.debug("{}".format(self.async_example))
        logger.error("{}".format(self.async_example))


    async def do_some_work(x):
        #print("AsyncExampleModel : Waiting " + str(x))
        logger.debug(" waiting {}".format(str(x)))
        await asyncio.sleep(x)


    def start_loop(self,loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()


    def more_work(self,x):
        logger.info("starting".format(x))
        time.sleep(x)

        my_auth0_controller = a0.Auth0Controller(logger)
        my_auth0_controller.ok_now_we_can_build_things()

        logger.info("finished".format(x))


    def log_work(self):
        logger.info("starting".format(4))
        time.sleep(4)
        logger.info("finished".format(4))


    '''
         https://hackernoon.com/threaded-asynchronous-magic-and-how-to-wield-it-bba9ed602c32
            # What if instead of doing everything in the current thread, we spawn a separate Thread to do the work for us.
            Notice that this time we created a new event loop through asyncio.new_event_loop(). The idea is to spawn a new thread, pass it that new loop and then call thread-safe functions (discussed later) to schedule work.

            The advantage of this method is that work executed by the other event loop will not block execution in the current thread. Thereby allowing the main thread to manage the work, and enabling a new category of execution mechanisms.
            '''
    def get_async_example_mgmt_access_token(self, protocol="https"):
        #print(" AsyncExampleModel running method get_async_example_mgmt_access_token")
        logger.debug(" {}" .format("."))

        new_loop = asyncio.new_event_loop()
        t = Thread(target=self.start_loop, args=(new_loop,))
        t.start()

        # it’s best to use their _threadsafe alternatives. Let’s see how that looks:

        new_loop.call_soon_threadsafe(self.more_work, 6)
        new_loop.call_soon_threadsafe(self.more_work, 3)


    def showloglevels(self, protocol="https"):
        logger.critical("Your program has done something awful")
        logger.error("Something has gone very wrong")
        logger.warning("You've been warned")
        logger.info("Here's some info")
        logger.debug("Debugging information")

        return "done with showloglevels"


    def call_worker_method(self, protocol="https"):
        logger.critical("Your program has done something awful")
        logger.error("Something has gone very wrong")
        logger.warning("You've been warned")
        logger.info("Here's some info")
        logger.debug("Debugging information")


