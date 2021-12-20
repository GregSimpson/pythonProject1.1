import asyncio
import http
import json
from _tracemalloc import start
from datetime import time
from time import sleep
from ..route import globals as gl

import logging
logger = logging.getLogger("RealplaySync")

class Auth0SyncModel:
    def __init__(self):
        self.auth0_sync = "auth0_sync Model!"
        #print("\n\t\tgjs >>> " +  self.auth0_sync)
        logger.debug("{}".format(self.auth0_sync))
        logger.debug("client_id variable     : {}".format(gl.client.id))
        logger.debug("client_secret variable : {}".format(gl.client.secret))


    def gjs1(self):
        logger.debug(" begin ")
        self.get_auth0_sync_mgmt_access_token()  #  works it just takes a while
        #asyncio.ensure_future( self.get_auth0_mgmt_access_token() )  #  testing a different example
        logger.debug(" end")



    def get_auth0_sync_mgmt_access_token(self, protocol="https"):
        logger.debug("begin")

        # management API access token
        conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
        payload = "{\"client_id\":\""+gl.client.id+"\",\"client_secret\":\""+gl.client.secret+"\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\",\"scope\":\"read:roles\",\"grant_type\":\"client_credentials\"}"
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

        print(" FINISHED method get_auth0_sync_mgmt_access_token")


    def get_auth0_mgmt_access_token_works(self):
        # management API access token
        conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
        payload = "{\"client_id\":\""+gl.client.id+"\",\"client_secret\":\""+gl.client.secret+"\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\",\"scope\":\"read:roles\",\"grant_type\":\"client_credentials\"}"
        headers = {'content-type': "application/json"}
        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)

        print (data)




    def gjs2(self, protocol="https"):
        import http.client

        conn = http.client.HTTPSConnection("")

        payload = "{\"client_id\":\""+gl.client.id+"\",\"client_secret\":\""+gl.client.secret+"\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\",\"scope\":\"read:roles\",\"grant_type\":\"client_credentials\"}"
        #&'audience=https://ttec-ped-developers.auth0.com/api/v2/' \
        #&scope=read:roles" \

        headers = {'content-type': "application/x-www-form-urlencoded"}
        domain="ttec-ped-developers.auth0.com"

        url = '{}://{}/oauth/token'.format(protocol, domain)
        #url = "https://ttec-ped-developers.auth0.com/oauth/token"

        logger.debug("url     : {} ".format(url))
        logger.debug("payload : {} ".format(payload))
        logger.debug("headers : {} ".format(headers))

        conn.request("POST", url, payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

