import asyncio
import http
import json
from _tracemalloc import start
from datetime import time
from time import sleep
from ..route import globals as gl

class Auth0SyncModel:
    def __init__(self):
        self.auth0_sync = "auth0_sync Model!"
        #print("\n\t\tgjs >>> " +  self.auth0_sync)
        print("\n\t\tAuth0SyncModel >>> {}".format(self.auth0_sync))
        print("\tini client_id variable     : {}".format(gl.client.id))
        print("\tini client_secret variable : {}".format(gl.client.secret))


    def gjs1(self):
        print(" running method gjs1")

        print(" firing : get_auth0_sync_mgmt_access_token")
        self.get_auth0_sync_mgmt_access_token()  #  works it just takes a while
        #asyncio.ensure_future( self.get_auth0_mgmt_access_token() )  #  testing a different example
        print(" gjs1 AFTER get_auth0_sync_mgmt_access_token - carrying on")



    def get_auth0_sync_mgmt_access_token(self, protocol="https"):
        print(" running method get_auth0_sync_mgmt_access_token")

        # management API access token
        conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
        payload = "{\"client_id\":\""+gl.client.id+"\",\"client_secret\":\""+gl.client.secret+"\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\",\"scope\":\"read:roles\",\"grant_type\":\"client_credentials\"}"
        headers = {'content-type': "application/json"}

        domain = "ttec-ped-developers.auth0.com"
        url = '{}://{}/oauth/token'.format(protocol, domain)
        print("\n")
        print("gjs-sync >> url     : {} ".format(url))
        print("gjs-sync >> payload : {} ".format(payload))
        print("gjs-sync >> headers : {} ".format(headers))
        print("\n")


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

        print("\n")
        print("gjs >> url     : {} ".format(url))
        print("\ngjs >> payload : {} ".format(payload))
        print("\ngjs >> headers : {} ".format(headers))
        print("\n")

        conn.request("POST", url, payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

