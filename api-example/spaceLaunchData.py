# https://holypython.com/api-5-space-launch-data/

# this api call works
import requests

f2 = r"https://launchlibrary.net/1.3/launch/2019-11-01"
#print(requests.get(f2).text)


#  I want to do something similar, but call to Ujet's api.
# Let's say the Agent api
#  in our case the api would be
# https://ttecphoenix-5x4khsz.uc1.ccaiplatform.com/manager/api/v1/agents
#

# UJET test
UJET_API = "https://ttecphoenix-5x4khsz.uc1.ccaiplatform.com/manager/api/v1/agents"
URL = UJET_API
USERNAME = "GregSimpson"
PASSWORD = "<api key pswd goes here>"

PARAMS = {'Username': USERNAME, 'Password' : PASSWORD}
HEADERS = {'Accept': 'application/vnd.json', 'User-Agent': "tap-ujet greg.simpson@ttec.com", 'Content-Type': 'application/json'}
METHOD = 'GET'


'''
response = self.__session.request(
                method=method,
                url=url,
                auth=(self.__company_key, self.__company_secret),
                json=json,
                **kwargs)
'''


g = requests.get(
    url=URL,
    auth=(USERNAME, PASSWORD),
    json=None)
print(g.json())

#r = requests.get(url=UJET_API, params=PARAMS, headers=HEADERS)
#print(r.json())
