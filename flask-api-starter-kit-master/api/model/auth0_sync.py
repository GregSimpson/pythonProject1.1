import asyncio
import http
import json
from _tracemalloc import start
from datetime import time
from time import sleep


class Auth0SyncModel:
    def __init__(self):
        self.auth0_sync = "auth0_sync Model!"
        #print("\n\t\tgjs >>> " +  self.auth0_sync)



    def gjs1(self):
        print(" running method gjs1")

        print(" firing : get_auth0_sync_mgmt_access_token")
        self.get_auth0_sync_mgmt_access_token()  #  works it just takes a while
        #asyncio.ensure_future( self.get_auth0_mgmt_access_token() )  #  testing a different example
        print(" gjs1 AFTER get_auth0_sync_mgmt_access_token - carrying on")



    def get_auth0_sync_mgmt_access_token(self):
        print(" running method get_auth0_sync_mgmt_access_token")

        # management API access token
        conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
        payload = "{\"client_id\":\"JmO3H4Y6WI3qhfe7Nu2j1ALecJ6U1nwo\",\"client_secret\":\"6C23kvixcwHffFHRVktSvxS2NYJemMgxBBfj6sRIUGgqRhgVClsiBd_HCFhUf4jo\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\",\"scope\":\"read:roles\",\"grant_type\":\"client_credentials\"}"
        headers = {'content-type': "application/json"}
        
        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)

        print (data)

        print(" FINISHED method get_auth0_sync_mgmt_access_token")


    def get_auth0_mgmt_access_token_works(self):
        # management API access token
        conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
        payload = "{\"client_id\":\"JmO3H4Y6WI3qhfe7Nu2j1ALecJ6U1nwo\",\"client_secret\":\"6C23kvixcwHffFHRVktSvxS2NYJemMgxBBfj6sRIUGgqRhgVClsiBd_HCFhUf4jo\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\",\"scope\":\"read:roles\",\"grant_type\":\"client_credentials\"}"
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

        payload = "grant_type=client_credentials&'client_id=JmO3H4Y6WI3qhfe7Nu2j1ALecJ6U1nwo'&client_secret=6C23kvixcwHffFHRVktSvxS2NYJemMgxBBfj6sRIUGgqRhgVClsiBd_HCFhUf4jo" # \
        #&'audience=https://ttec-ped-developers.auth0.com/api/v2/' \
        #&scope=read:roles" \

        ##payload = "grant_type=client_credentials&client_id=%24%7Baccount.clientId%7D&client_secret=YOUR_CLIENT_SECRET&audience=https%3A%2F%2F%24%7Baccount.namespace%7D%2Fapi%2Fv2%2F"

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

