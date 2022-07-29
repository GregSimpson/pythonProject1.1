# https://holypython.com/api-5-space-launch-data/

# this api call works
import requests
f2 = r"https://launchlibrary.net/1.3/launch/2019-11-01"
print(requests.get(f2).text)


#  I want to do something similar, but call to Ujet's api.
# Let's say the Agent api
#  in our case the api would be
# https://ttecphoenix-5x4khsz.uc1.ccaiplatform.com/manager/api/v1/agents
#

# UJET test
UJET_API = "https://ttecphoenix-5x4khsz.uc1.ccaiplatform.com/manager/api/v1/agents"
USERNAME = "GregSimpson"
PASSWORD = "yzsJpktWH2bfnGPz94DtHH6_3UYaO88TDKrLFFe5VR0"

PARAMS = {'Username': USERNAME, 'Password' : PASSWORD}
r = requests.get(url=UJET_API, params=PARAMS)
print(r.json())
