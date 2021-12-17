import asyncio

import http
import time
from threading import Thread


class Auth0AsyncModel:
    def __init__(self):
        self.auth0_async = 'auth0_async'
        print("\n\t\tAuth0AsyncModel >>> {}".format(self.auth0_async))

    async def do_some_work(x):
        print("Auth0AsyncModel : Waiting " + str(x))
        await asyncio.sleep(x)

    def start_loop(self,loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def more_work(self,x):
        print("Auth0AsyncModel : More work %s" % x)
        time.sleep(x)
        print("Auth0AsyncModel : Finished more work %s" % x)

    def start_loop(self,loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def get_auth0_async_mgmt_access_token(self, protocol="https"):
        print(" Auth0AsyncModel running method get_auth0_async_mgmt_access_token")

        # management API access token
        conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
        payload = "{\"client_id\":\"<client idcode>\",\"client_secret\":\"<client secret code>\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\",\"scope\":\"read:roles\",\"grant_type\":\"client_credentials\"}"
        headers = {'content-type': "application/json"}
        domain = "ttec-ped-developers.auth0.com"

        url = '{}://{}/oauth/token'.format(protocol, domain)
        # url = "https://ttec-ped-developers.auth0.com/oauth/token"

        print("\nAuth0AsyncModel")
        print("gjs-async >> url     : {} ".format(url))
        print("gjs-async >> payload : {} ".format(payload))
        print("gjs-async >> headers : {} ".format(headers))
        print("\nAuth0AsyncModel")
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
=======
        conn = http.client.HTTPSConnection("")

        payload = "grant_type=client_credentials&'client_id=<client idcode >'&client_secret=<client  secret code >" # \
        #&'audience=https://ttec-ped-developers.auth0.com/api/v2/' \
        #&scope=read:roles" \

        headers = {'content-type': "application/x-www-form-urlencoded"}
        domain="ttec-ped-developers.auth0.com"


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


