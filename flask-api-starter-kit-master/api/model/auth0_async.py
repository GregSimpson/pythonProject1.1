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


class Auth0AsyncModel:
    def __init__(self):
        self.auth0_async = 'auth0_async'
        logger.debug("{}".format(self.auth0_async))
        logger.debug("ini client_id variable     : {}".format(gl.client.id))
        logger.debug("ini client_secret variable : {}".format(gl.client.secret))

    async def do_some_work(x):
        logger.debug("Waiting {}".format(str(x)))
        await asyncio.sleep(x)

    def start_loop(self,loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def more_work(self,x):
        logger.debug("starting {}".format(str(x)))
        time.sleep(x)
        logger.debug("finished {}".format(str(x)))

#    def start_loop(self,loop):
#        asyncio.set_event_loop(loop)
#        loop.run_forever()

    def get_auth0_async_mgmt_access_token(self, protocol="https"):
        logger.debug(" {} ".format("."))

        # management API access token
        conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
        payload = "{\"client_id\":\"" + gl.client.id + "\",\"client_secret\":\"" + gl.client.secret + "\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\",\"scope\":\"read:roles\",\"grant_type\":\"client_credentials\"}"
        headers = {'content-type': "application/json"}

        domain = "ttec-ped-developers.auth0.com"
        url = '{}://{}/oauth/token'.format(protocol, domain)
        logger.debug("url     : {} ".format(url))
        logger.debug("payload : {} ".format(payload))
        logger.debug("headers : {} ".format(headers))

        '''
        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)

        print (data)
        '''


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

        ##new_loop.close()
        #client.close()


