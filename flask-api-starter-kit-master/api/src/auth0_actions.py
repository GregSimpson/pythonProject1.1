import asyncio
import json
import time
from threading import Thread
import os

import http
from ..route import globals as gl

import logging
logger = logging.getLogger("RealplaySync")


class Auth0Actions:
	def __init__(self):
		self.auth0_actions = 'auth0_actions'

	def start_loop(self, loop):
		asyncio.set_event_loop(loop)
		loop.run_forever()

	def x_step1_get_auth0_certificate(self):
		logger.debug(" gjs begin ")

		# nested list
		cert_list = ["title", [8, "four", 6], ['a']]
		logger.debug("cert_list : \n{}".format(cert_list))
		logger.debug("  gjs end  ")

		return cert_list


	def step1_get_auth0_certificate(self, protocol="https"):
		logger.debug(" {} ".format("."))

		# management API access token
		conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
		payload = "{\"client_id\":\"" + gl.client.id + "\",\"client_secret\":\"" + gl.client.secret + "\",\"audience\":\"" + protocol+ "://" + gl.client.domain + gl.auth0.url_get_token
		headers = {'content-type': "application/json"}

		url = '{}://{}/oauth/token'.format(protocol, gl.client.domain)
		logger.debug("url     : {} ".format(url))
		logger.debug("gl.client.domain : \n{} ".format(gl.client.domain))
		logger.debug("payload : \n{} ".format(payload))
		logger.debug("headers : {} ".format(headers))

		'''  '''
		conn.request("POST", "/oauth/token", payload, headers)
		res = conn.getresponse()
		data = res.read()
		data = data.decode("utf-8")
		data = json.loads(data)

		#print (data)
		return data

		''' '''


	# https://auth0.com/docs/organizations/configure/retrieve-organizations
	def retrieve_organizations(self,auth0_certificate):
		logger.debug("auth0_certificate\n{}\n".format(auth0_certificate))
		logger.debug("auth0_certificate - access-token\n{}\n".format(auth0_certificate['access_token']))


		#conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
		#conn = http.client.HTTPSConnection("realplayserver.dce1.humanify.com")


		#conn = http.client.HTTPSConnection("")
		#https: // realplayserver.dce1.humanify.com / tenants /
		#payload = "{\"client_id\":\"" + gl.client.id + "\",\"client_secret\":\"" + gl.client.secret + "\",\"audience\":\"https://ttec-ped-developers.auth0.com/api/v2/\"}"
		#payloadx = "{\"client_id\":\"" + gl.client.id + "\",\"client_secret\":\"" + gl.client.secret + "\",\"audience\":\"https://realplayserver.dce1.humanify.com/\"}"
		#headers = {'content-type': 'application/json','Authorization': 'Bearer {}'.format(auth0_certificate)}

		#import http.client
		#conn = http.client.HTTPSConnection("")
		#conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
		#conn = http.client.HTTPSConnection("realplayserver.dce1.humanify.com")
		#conn = http.client.HTTPSConnection("realplayserver.dce1.humanify.com")

		#headers = {'authorization': str(auth0_certificate) }
		#headers = {'authorization': "Bearer {}".format(auth0_certificate) }
		#headers = {'authorization': "{}".format(auth0_certificate)}
		#headers = {'Authorization': 'Bearer {}'.format(auth0_certificate)}
		#headers = {'authorization: {}'.format(auth0_certificate)}

		# --header 'authorization: Bearer MGMT_API_ACCESS_TOKEN'

		#headers["Authorization"] = "Bearer {}".format(auth0_certificate)
		#
		#logger.debug("\npayloadx {}\n".format(payloadx))
		#conn.request("GET", "https://ttec-ped-developers.auth0.com/tenants/", headers=headers)
		#conn.request("GET", "/tenants", payloadx, headers)
		#conn.request("POST", "/oauth/token", payload, headers)
		#/ oauth / token
		#conn.request("GET", "https://realplayserver.dce1.humanify.com/tenants/", headers=headers)

		headers = {'authorization': '{}'.format(auth0_certificate)}
		logger.debug("headers --\n{}\n--".format(headers))
		#conn = http.client.HTTPConnection("realplayserver.dce1.humanify.com")
		conn = http.client.HTTPSConnection("realplayserver.dce1.humanify.com")

		#conn.request("GET", "/tenants", headers=headers)
		conn.request("GET", "/users", headers=headers)
		res = conn.getresponse()
		data = res.read()
		logger.debug(data)

		##print(data.decode("utf-8"))
		#logger.debug("\ndata = {}\n".format(data))
		#logger.debug("\ndata = {}\n".format(data.decode("utf-8")))



	def step2_get_auth0_tenants(self, auth0_certificate,protocol="https"):
		logger.debug(" {} ".format("."))

		import http.client
		conn = http.client.HTTPSConnection("")
		headers = {'authorization': "Bearer MGMT_API_ACCESS_TOKEN"}
		conn.request("GET", "/YOUR_DOMAIN/api/v2/organizations/ORG_ID/members", headers=headers)

		res = conn.getresponse()
		data = res.read()

		print(data.decode("utf-8"))


	##def sx-step2_get_auth0_tenants(self, cert_dict):
#		logger.debug(" begin ")###
#
#		# nested list#
#		tenant_list = ["mouse", [8, 4, 6], ['a']]
#
#		logger.debug(" 		cert_dict : \n{}".format(cert_dict))
#		logger.debug(" 		return tenant_list : \n{}".format(tenant_list ))
#		logger.debug("  end  ")
#		return tenant_list


	def step3_get_auth0_users_by_tenant(self):
		logger.debug(" begin ")

		tenant_users_dict = {
			"BOA": ["boa_user11","boa_user12","boa_user13"],
			"Ford": ["ford_user21", "ford_user22", "ford_user23"],
			"Parasol": ["parasol_user31", "parasol_user32", "parasol_user33"]
		}

		logger.debug(" tenant_users_dict : \n{}".format(tenant_users_dict))
		logger.debug("  end  ")
		return tenant_users_dict

	def step4_get_auth0_roles_by_user(self):
		logger.debug(" begin ")

		tenant_users_roles_dict = {
			"BOA": {
				"boa_user11":["boa_role11_1","boa_role11_2","boa_role11_3","boa_role11_4"],
				"boa_user12":["boa_role12_1","boa_role12_2","boa_role12_3","boa_role12_4"],
				"boa_user13":["boa_role13_1","boa_role13_2","boa_role13_3","boa_role13_4"]
			},
			"Ford": {
				"ford_user11": ["ford_role11_1"],
				"ford_user12": ["ford_role12_1", "ford_role12_2"],
				"ford_user13": ["ford_role13_1", "ford_role13_2", "ford_role13_3"],
				"ford_user14": ["ford_role14_1", "ford_role14_2", "ford_role14_3", "ford_role14_4"]
			},
			"Parasol": {
				"parasol_user11": ["parasol_role11_1", "parasol_role11_2", "parasol_role11_3", "parasol_role11_4"],
				"parasol_user12": ["parasol_role12_1", "parasol_role12_2", "parasol_role12_3", "parasol_role12_4"],
				"parasol_user13": ["parasol_role13_1", "parasol_role13_2", "parasol_role13_3", "parasol_role13_4"]
			}
		}

		logger.debug(" tenant_users_roles_dict : \n{}".format(tenant_users_roles_dict))
		logger.debug("  end  ")
		return tenant_users_roles_dict



	def ok_now_we_can_build_things(self):
		logger.debug("step1 - get Auth0 Certificate")
		logger.debug("step2 - get Auth0 tenants")
		logger.debug("step3 - for each tenant, get userlist")
		logger.debug("step4 - for each tenant-user, get role data")