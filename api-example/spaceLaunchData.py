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


# UJET test apis
USERNAME = "GregSimpson"
PASSWORD = "yzsJpktWH2bfnGPz94DtHH6_3UYaO88TDKrLFFe5VR0"
PARAMS = {'Username': USERNAME, 'Password' : PASSWORD}
HEADERS = {'Accept': 'application/vnd.json', 'User-Agent': "tap-ujet greg.simpson@ttec.com", 'Content-Type': 'application/json'}
METHOD = 'GET'

# GET APIs
# Manager APIs
UJET_BASE = "https://ttecphoenix-5x4khsz.uc1.ccaiplatform.com/manager/api/v1/"

# Agents
UJET_API = "agents"
# Agents Activity Logs
#UJET_API = "agent_activity_logs"
# Agents Current Status
#UJET_API = "agents/current_status"
# Calls
#UJET_API = "calls"
# Chats
#UJET_API = "chats"
# User Statuses
#UJET_API = "user_statuses"
# Teams
#UJET_API = "teams"
# Single Team
#UJET_API = "teams/1"
# Team Tree
#UJET_API = "teams/tree"

# APPS APIs
UJET_BASE = "https://ttecphoenix-5x4khsz.uc1.ccaiplatform.com/apps/api/v1/"
UJET_API = "wait_times?lang=en"

URL = UJET_BASE + UJET_API


HEADERS = { \
    'Content-Length': '0', \
    'User-Agent': "tap-ujet greg.simpson@ttec.com", \
    'Accept': '*/*', \
    'Accept-Encoding': 'gzip, deflate, br', \
    'Connection': 'keep-alive' \
    }

print(URL)
print(USERNAME)
print(PASSWORD)
print(HEADERS)

g = requests.get(
    url=URL,
    auth=(USERNAME, PASSWORD),
    json=None,
    headers=HEADERS)
print(g.json())

'''
# PUT APIs
UJET_BASE = "https://ttecphoenix-5x4khsz.uc1.ccaiplatform.com/apps/api/v1/"

# Outbound call
UJET_API = "calls?lang=en"
# Incoming Call
#UJET_API = "calls?lang=en"
# Outbound SMS
#UJET_API = "calls"
# CRM Contact Data
#UJET_API = "crm_contact_cdata?lang=en"

URL = UJET_BASE + UJET_API

HEADERS = { \
    'Content-Length': '0', \
    'User-Agent': "PostmanRuntime/7.29.2", \
    'Accept': '*/*', \
    'Accept-Encoding': 'gzip, deflate, br', \
    'Connection': 'keep-alive' \
    }

print(URL)
print(USERNAME)
print(PASSWORD)
print(HEADERS)

g = requests.put(
    url=URL,
    auth=(USERNAME, PASSWORD),
    json=None,
    headers=HEADERS
)
print(g)
'''
#r = requests.get(url=UJET_API, params=PARAMS, headers=HEADERS)
#print(r.json())
