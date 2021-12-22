import asyncio
import json
import time
from threading import Thread
import os

#import auth0
#from auth0.v3.management import Auth0
#rom auth0.v3.authentication import GetToken

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



	# https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
	def export_users(self,auth0_certificate):
		logger.debug("auth0_certificate\n{}\n".format(auth0_certificate))
		logger.debug("auth0_certificate - access-token\n{}\n".format(auth0_certificate['access_token']))

		headers = {'authorization': '{}'.format(auth0_certificate)}
		logger.debug("headers --\n{}\n--".format(headers))
		#conn = http.client.HTTPSConnection("realplayserver.dce1.humanify.com")
		#conn = http.client.HTTPSConnection("realplayserver.dce1.humanify.com")
		conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")

		#  these sort of work , but stop at a 'redirect' message
		#conn.request("GET", "/tenants", headers=headers)
		#conn.request("GET", "/users", headers=headers)
		bodyparam = "{123}"
		#conn.request("POST", "/api/v2/jobs/users-exports", headers=headers, json=bodyparam)
		conn.request("POST", "/jobs/users-exports", headers=headers)


		res = conn.getresponse()
		data = res.read()
		logger.debug(data)

	'''
	import http.client
	conn = http.client.HTTPConnection("path_to_your_api")
	headers = { 'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9ESTBuak94MnBBckUtMW8tVUNnaiJ9.eyJpc3MiOiJodHRwczovL3R0ZWMtcGVkLWRldmVsb3BlcnMuYXV0aDAuY29tLyIsInN1YiI6IkptTzNINFk2V0kzcWhmZTdOdTJqMUFMZWNKNlUxbndvQGNsaWVudHMiLCJhdWQiOiJodHRwczovL3R0ZWMtcGVkLWRldmVsb3BlcnMuYXV0aDAuY29tL2FwaS92Mi8iLCJpYXQiOjE2NDAxOTIwNTUsImV4cCI6MTY0MDI3ODQ1NSwiYXpwIjoiSm1PM0g0WTZXSTNxaGZlN051MmoxQUxlY0o2VTFud28iLCJzY29wZSI6InJlYWQ6Y2xpZW50X2dyYW50cyBjcmVhdGU6Y2xpZW50X2dyYW50cyBkZWxldGU6Y2xpZW50X2dyYW50cyB1cGRhdGU6Y2xpZW50X2dyYW50cyByZWFkOnVzZXJzIHVwZGF0ZTp1c2VycyBkZWxldGU6dXNlcnMgY3JlYXRlOnVzZXJzIHJlYWQ6dXNlcnNfYXBwX21ldGFkYXRhIHVwZGF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgZGVsZXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBjcmVhdGU6dXNlcnNfYXBwX21ldGFkYXRhIHJlYWQ6dXNlcl9jdXN0b21fYmxvY2tzIGNyZWF0ZTp1c2VyX2N1c3RvbV9ibG9ja3MgZGVsZXRlOnVzZXJfY3VzdG9tX2Jsb2NrcyBjcmVhdGU6dXNlcl90aWNrZXRzIHJlYWQ6Y2xpZW50cyB1cGRhdGU6Y2xpZW50cyBkZWxldGU6Y2xpZW50cyBjcmVhdGU6Y2xpZW50cyByZWFkOmNsaWVudF9rZXlzIHVwZGF0ZTpjbGllbnRfa2V5cyBkZWxldGU6Y2xpZW50X2tleXMgY3JlYXRlOmNsaWVudF9rZXlzIHJlYWQ6Y29ubmVjdGlvbnMgdXBkYXRlOmNvbm5lY3Rpb25zIGRlbGV0ZTpjb25uZWN0aW9ucyBjcmVhdGU6Y29ubmVjdGlvbnMgcmVhZDpyZXNvdXJjZV9zZXJ2ZXJzIHVwZGF0ZTpyZXNvdXJjZV9zZXJ2ZXJzIGRlbGV0ZTpyZXNvdXJjZV9zZXJ2ZXJzIGNyZWF0ZTpyZXNvdXJjZV9zZXJ2ZXJzIHJlYWQ6ZGV2aWNlX2NyZWRlbnRpYWxzIHVwZGF0ZTpkZXZpY2VfY3JlZGVudGlhbHMgZGVsZXRlOmRldmljZV9jcmVkZW50aWFscyBjcmVhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIHJlYWQ6cnVsZXMgdXBkYXRlOnJ1bGVzIGRlbGV0ZTpydWxlcyBjcmVhdGU6cnVsZXMgcmVhZDpydWxlc19jb25maWdzIHVwZGF0ZTpydWxlc19jb25maWdzIGRlbGV0ZTpydWxlc19jb25maWdzIHJlYWQ6aG9va3MgdXBkYXRlOmhvb2tzIGRlbGV0ZTpob29rcyBjcmVhdGU6aG9va3MgcmVhZDphY3Rpb25zIHVwZGF0ZTphY3Rpb25zIGRlbGV0ZTphY3Rpb25zIGNyZWF0ZTphY3Rpb25zIHJlYWQ6ZW1haWxfcHJvdmlkZXIgdXBkYXRlOmVtYWlsX3Byb3ZpZGVyIGRlbGV0ZTplbWFpbF9wcm92aWRlciBjcmVhdGU6ZW1haWxfcHJvdmlkZXIgYmxhY2tsaXN0OnRva2VucyByZWFkOnN0YXRzIHJlYWQ6aW5zaWdodHMgcmVhZDp0ZW5hbnRfc2V0dGluZ3MgdXBkYXRlOnRlbmFudF9zZXR0aW5ncyByZWFkOmxvZ3MgcmVhZDpsb2dzX3VzZXJzIHJlYWQ6c2hpZWxkcyBjcmVhdGU6c2hpZWxkcyB1cGRhdGU6c2hpZWxkcyBkZWxldGU6c2hpZWxkcyByZWFkOmFub21hbHlfYmxvY2tzIGRlbGV0ZTphbm9tYWx5X2Jsb2NrcyB1cGRhdGU6dHJpZ2dlcnMgcmVhZDp0cmlnZ2VycyByZWFkOmdyYW50cyBkZWxldGU6Z3JhbnRzIHJlYWQ6Z3VhcmRpYW5fZmFjdG9ycyB1cGRhdGU6Z3VhcmRpYW5fZmFjdG9ycyByZWFkOmd1YXJkaWFuX2Vucm9sbG1lbnRzIGRlbGV0ZTpndWFyZGlhbl9lbnJvbGxtZW50cyBjcmVhdGU6Z3VhcmRpYW5fZW5yb2xsbWVudF90aWNrZXRzIHJlYWQ6dXNlcl9pZHBfdG9rZW5zIGNyZWF0ZTpwYXNzd29yZHNfY2hlY2tpbmdfam9iIGRlbGV0ZTpwYXNzd29yZHNfY2hlY2tpbmdfam9iIHJlYWQ6Y3VzdG9tX2RvbWFpbnMgZGVsZXRlOmN1c3RvbV9kb21haW5zIGNyZWF0ZTpjdXN0b21fZG9tYWlucyB1cGRhdGU6Y3VzdG9tX2RvbWFpbnMgcmVhZDplbWFpbF90ZW1wbGF0ZXMgY3JlYXRlOmVtYWlsX3RlbXBsYXRlcyB1cGRhdGU6ZW1haWxfdGVtcGxhdGVzIHJlYWQ6bWZhX3BvbGljaWVzIHVwZGF0ZTptZmFfcG9saWNpZXMgcmVhZDpyb2xlcyBjcmVhdGU6cm9sZXMgZGVsZXRlOnJvbGVzIHVwZGF0ZTpyb2xlcyByZWFkOnByb21wdHMgdXBkYXRlOnByb21wdHMgcmVhZDpicmFuZGluZyB1cGRhdGU6YnJhbmRpbmcgZGVsZXRlOmJyYW5kaW5nIHJlYWQ6bG9nX3N0cmVhbXMgY3JlYXRlOmxvZ19zdHJlYW1zIGRlbGV0ZTpsb2dfc3RyZWFtcyB1cGRhdGU6bG9nX3N0cmVhbXMgY3JlYXRlOnNpZ25pbmdfa2V5cyByZWFkOnNpZ25pbmdfa2V5cyB1cGRhdGU6c2lnbmluZ19rZXlzIHJlYWQ6bGltaXRzIHVwZGF0ZTpsaW1pdHMgY3JlYXRlOnJvbGVfbWVtYmVycyByZWFkOnJvbGVfbWVtYmVycyBkZWxldGU6cm9sZV9tZW1iZXJzIHJlYWQ6ZW50aXRsZW1lbnRzIHJlYWQ6YXR0YWNrX3Byb3RlY3Rpb24gdXBkYXRlOmF0dGFja19wcm90ZWN0aW9uIHJlYWQ6b3JnYW5pemF0aW9ucyB1cGRhdGU6b3JnYW5pemF0aW9ucyBjcmVhdGU6b3JnYW5pemF0aW9ucyBkZWxldGU6b3JnYW5pemF0aW9ucyBjcmVhdGU6b3JnYW5pemF0aW9uX21lbWJlcnMgcmVhZDpvcmdhbml6YXRpb25fbWVtYmVycyBkZWxldGU6b3JnYW5pemF0aW9uX21lbWJlcnMgY3JlYXRlOm9yZ2FuaXphdGlvbl9jb25uZWN0aW9ucyByZWFkOm9yZ2FuaXphdGlvbl9jb25uZWN0aW9ucyB1cGRhdGU6b3JnYW5pemF0aW9uX2Nvbm5lY3Rpb25zIGRlbGV0ZTpvcmdhbml6YXRpb25fY29ubmVjdGlvbnMgY3JlYXRlOm9yZ2FuaXphdGlvbl9tZW1iZXJfcm9sZXMgcmVhZDpvcmdhbml6YXRpb25fbWVtYmVyX3JvbGVzIGRlbGV0ZTpvcmdhbml6YXRpb25fbWVtYmVyX3JvbGVzIGNyZWF0ZTpvcmdhbml6YXRpb25faW52aXRhdGlvbnMgcmVhZDpvcmdhbml6YXRpb25faW52aXRhdGlvbnMgZGVsZXRlOm9yZ2FuaXphdGlvbl9pbnZpdGF0aW9ucyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyJ9.SrRcnlhI1feZ-oODfirCPd6r7uXxqzK45HKJpD4WYIT5V4Quj-lhqCF0t1Fz7XvbIlJ6qvx4iRBoHbamTl1IGgqpWnXVGz2AUpHs2ON8PW9l2MLIcxkdJtHbgGh2JOe7qLOWBr5PC-MJeL-EcP1STN9JDst89LaZ05g0790nT2__P4n1y15TxZLQzQQYBIZA4QbW0SDrGQPeyNHyS58A-LO8KCuvRkyFjKvpdWukPLHECD6JwKSXQp9qllIpwOL9WFmJbb9fkQjkRVwm2c0OFlQ202R2grWKr3sFH5I7fa8a3LYMXktYyO8AnoeANbXEgNtCuOVjbaIYe0hZXL3HGA" }
	conn.request("GET", "/", headers=headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))
	'''

	# https://github.com/auth0/auth0-python#management-sdk
	# pip3 install auth0-python

	def github_example(self, auth0_certificate):
		#from auth0.v3.authentication import GetToken

		#domain = 'myaccount.auth0.com'
		domain = 'ttec-ped-developers.auth0.com'
		non_interactive_client_id = gl.client.id
		non_interactive_client_secret = gl.client.secret

		#get_token = GetToken(domain)
		token = get_token.client_credentials(non_interactive_client_id,
		                                     non_interactive_client_secret, 'https://{}/api/v2/'.format(domain))
		mgmt_api_token = token['access_token']

		# then use the new token
		# from auth0.v3.management import Auth0

		##domain = 'myaccount.auth0.com'
		##mgmt_api_token = 'MGMT_API_TOKEN'

		#auth0 = Auth0(domain, mgmt_api_token)

		# The Auth0 object is now ready to take orders! Let's see how we can use this to get all available connections
		# (this action requires the token to have the following scope: read:connections)
		logger.debug("\n{}\n".format(auth0.connections.all()))
		return auth0.connections.all()






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
		conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
		#conn = http.client.HTTPSConnection("realplayserver.dce1.humanify.com")

		#conn.request("GET", "/tenants", headers=headers)
		#conn.request("GET", "/users", headers=headers)

		#conn.request("GET", "/ttec-ped-developers.auth0.com/api/v2/users/USER_ID/roles", headers=headers)

		conn.request("GET", "/api/v2/users/auth0|6018408ed01fc80071cd4564/roles", headers=headers)
		                            #auth0|6018408ed01fc80071cd4564
		res = conn.getresponse()
		data = res.read()
		logger.debug(data)

		##print(data.decode("utf-8"))
		#logger.debug("\ndata = {}\n".format(data))
		#logger.debug("\ndata = {}\n".format(data.decode("utf-8")))


	#retrieve_userdata
	def retrieve_userdata(self,auth0_certificate):
		#logger.debug("auth0_certificate\n{}\n".format(auth0_certificate))
		#logger.debug("auth0_certificate - access-token\n{}\n".format(auth0_certificate['access_token']))


		#headers = {'authorization: Bearer {}'.format(auth0_certificate)}
		headers = {'authorization': 'Bearer {}'.format(auth0_certificate['access_token'])}
		#headers = {'authorization: Bearer {}'.format(auth0_certificate)}
		logger.debug("headers --\n{}\n--".format(headers))
		conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
		conn.request("GET", "/api/v2/users/auth0|6018408ed01fc80071cd4564/roles", headers=headers)
		###logger.debug("USER RESULTS\n++++\n{}\n++++\n".format(conn.getresponse()))

		res = conn.getresponse()
		data = res.read()
		logger.debug(data)

		my_json = json.loads(data)
		logger.debug( json.dumps(my_json, indent=2))

	### https://ttec-ped-developers.us12.webtask.io/auth0-user-import-export/api/jobs/export
	def export_userlist(self, auth0_certificate):
		#logger.debug("auth0_certificate\n{}\n".format(auth0_certificate))
		#logger.debug("auth0_certificate - access-token\n{}\n".format(auth0_certificate['access_token']))

		# Authorization: Bearer [token]
		headers = {'Authorization': 'Bearer {}'.format(auth0_certificate['access_token'])}
		#headers = {'{}'.format(auth0_certificate['access_token'])}

		# headers = {'Authorization: Bearer {}'.format(auth0_certificate)}
		# headers = {'Authorization: Bearer {}'.format(auth0_certificate['access_token'])}
		logger.debug("headers --\n{}\n--".format(headers))
		### conn = http.client.HTTPConnection("realplayserver.dce1.humanify.com")
		conn = http.client.HTTPSConnection("ttec-ped-developers.us12.webtask.io")
		#conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")

		body_payload={'some':'123'}

		#conn.request("POST", "/auth0-user-import-export/api/jobs/export", headers=headers)
		conn.request("POST", "/auth0-user-import-export/api/jobs/export", headers=headers, body=json.dumps(body_payload))
		res = conn.getresponse()
		data = res.read()
		logger.debug(data)

	# https://auth0.com/docs/users/import-and-export-users/bulk-user-exports
	# https://community.auth0.com/t/users-exports-returning-404/58599/2
	def gjs_example(self, auth0_certificate):
		import http.client
		conn = http.client.HTTPSConnection("")
		payload = "{\"connection_id\": \"con_oOFR9nEz36wvZIXI\", \"format\": \"json\", \"limit\": 5, \"fields\": [{\"name\": \"email\"}, { \"name\": \"identities[0].connection\", \"export_as\": \"provider\" }]}"
		headers = {
			#'authorization': "Bearer YOUR_MGMT_API_ACCESS_TOKEN",
			'authorization': "Bearerx {}".format(auth0_certificate['access_token']),
			'content-type': "application/json"
		}
		#conn.request("POST", "/ttec-ped-developers.auth0.com/api/v2/jobs/users-exports", payload, headers)
		conn.request("GET", "/ttec-ped-developers.auth0.com/api/v2/", payload, headers)
		res = conn.getresponse()
		data = res.read()
		print(data.decode("utf-8"))


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