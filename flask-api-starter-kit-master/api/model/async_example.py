import asyncio
import time
from threading import Thread


import logging
#logging.basicConfig(level=logging.INFO)
##logger = logging.getLogger(__name__)
logger = logging.getLogger("RealplaySync")

'''
#-----
import os
import logging.config

import yaml


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


#-----
'''

class AsyncExampleModel:
    def __init__(self):
        self.async_example = 'async_example'

        ###setup_logging()
        #### #logger = logging.getLogger("RealplaySync")

        #print("\n\t\tgjs >>> {}".format(self.async_example))
        logger.debug("\n\t\t!!!!! gjs >>> {}".format(self.async_example))
        logger.error("\n\t\t!!!!! gjs >>> {}".format(self.async_example))

    async def do_some_work(x):
        #print("AsyncExampleModel : Waiting " + str(x))
        logger.debug("AsyncExampleModel : do_some_work " + str(x))
        await asyncio.sleep(x)

    def start_loop(self,loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def more_work(self,x):
        #print("AsyncExampleModel : More work %s" % x)
        logger.info("AsyncExampleModel : More work %s" % x)
        time.sleep(x)
        #print("AsyncExampleModel : Finished more work %s" % x)
        logger.debug("AsyncExampleModel : Finished more work %s" % x)

    def start_loop(self,loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    '''
         https://hackernoon.com/threaded-asynchronous-magic-and-how-to-wield-it-bba9ed602c32
            # What if instead of doing everything in the current thread, we spawn a separate Thread to do the work for us.
            Notice that this time we created a new event loop through asyncio.new_event_loop(). The idea is to spawn a new thread, pass it that new loop and then call thread-safe functions (discussed later) to schedule work.

            The advantage of this method is that work executed by the other event loop will not block execution in the current thread. Thereby allowing the main thread to manage the work, and enabling a new category of execution mechanisms.
            '''
    def get_async_example_mgmt_access_token(self, protocol="https"):
        #print(" AsyncExampleModel running method get_async_example_mgmt_access_token")
        logger.debug(" AsyncExampleModel running method get_async_example_mgmt_access_token")

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


