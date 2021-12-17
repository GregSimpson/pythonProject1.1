import asyncio
import http
import json
from _tracemalloc import start
from datetime import time
from time import sleep


class Auth0AsyncModel:
    def __init__(self):
        self.auth0_async = 'auth0_async'
        print("\n\t\tgjs >>> {}".format(self.auth0_async))



    def gjs1(self):
        print(" running method gjs1")

        print(" firing : get_auth0_async_mgmt_access_token")
        #self.get_auth0_async_mgmt_access_token()  #  works it just takes a while
        #asyncio.ensure_future( self.get_auth0_async_mgmt_access_token() )  #  testing a different example
        print(" gjs1 AFTER get_auth0_async_mgmt_access_token - carrying on")



    def get_auth0_async_mgmt_access_token(self, protocol="https"):
        print(" running method get_auth0_async_mgmt_access_token")

        # management API access token
        conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
        payload = "{\"client_id\":\"<client idcode >\",\"client_secret\":\"<client secret code >\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\",\"scope\":\"read:roles\",\"grant_type\":\"client_credentials\"}"
        headers = {'content-type': "application/json"}

        domain = "ttec-ped-developers.auth0.com"

        url = '{}://{}/oauth/token'.format(protocol, domain)
        # url = "https://ttec-ped-developers.auth0.com/oauth/token"

        print("\n")
        print("gjs-async >> url     : {} ".format(url))
        print("\ngjs-async >> payload : {} ".format(payload))
        print("\ngjs-async >> headers : {} ".format(headers))
        print("\n")
        '''
        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)

        print (data)
        '''

        print(" FINISHED method get_auth0_async_mgmt_access_token")






    def gjs2(self, protocol="https"):
        import http.client

        conn = http.client.HTTPSConnection("")

        payload = "grant_type=client_credentials&'client_id=<client idcode >'&client_secret=<client  secret code >" # \
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

