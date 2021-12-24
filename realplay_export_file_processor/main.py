import http
import json
from pathlib import Path
from datetime import datetime
import logging.config
import os

import yaml
from flask import Flask
import configparser
import pandas as pd

# open a terminal 'at the bottom of intellij'
# pip install psycopg2-binary
import psycopg2


def test_log_messages():
	logger.debug('test msg')
	logger.info('test msg')
	logger.warning('test msg')
	logger.error('test msg')
	logger.critical('test msg')

	logger.debug('setting test : {}'.format(parser.get('ttec-realplay-parasol', 'client_domain')))


def setup_logging():
	with open('./conf/logging.yaml', 'r') as stream:
		config = yaml.load(stream, Loader=yaml.FullLoader)
	logging.config.dictConfig(config)



def load_settings():
	# https://www.tutorialspoint.com/configuration-file-parser-in-python-configparser
	# parser = configparser.ConfigParser()
	parser.read('conf/settings.ini')
	for sect in parser.sections():
		logger.info('Section: {}'.format(sect))
		for k, v in parser.items(sect):
			logger.info(' {} = {}'.format(k, v))
		logger.info(' ')


def create_app():
	app = Flask(__name__)

	#output_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
	#output_dir.mkdir(parents=True, exist_ok=True)
	setup_logging()
	load_settings()

	return app


def step1_get_auth0_certificate(client_domain_param, protocol="https"):
	logger.debug("client_domain_param: {} :: protocol: {}".format(client_domain_param, protocol))

	# management API access token
	conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")
	#payload = "{\"client_id\":\"" + gl.client.id + "\",\"client_secret\":\"" + gl.client.secret + "\",\"audience\":\"" + protocol + "://" + gl.client.domain + gl.auth0.url_get_token
	payload = "{\"client_id\":\"" + parser.get(client_domain_param, 'client_id') + "\",\"client_secret\":\"" + parser.get(client_domain_param, 'client_secret') + "\",\"audience\":\"" + protocol + "://" + parser.get(client_domain_param, 'client_domain') + parser.get('Auth0Info', 'url_get_token')
	headers = {'content-type': "application/json"}

	url = '{}://{}/oauth/token'.format(protocol, parser.get(client_domain_param, 'client_domain'))
	logger.debug("url     : {} ".format(url))
	logger.debug("gl.client.domain : \n{} ".format(parser.get(client_domain_param, 'client_domain')))
	logger.debug("payload : \n{} ".format(payload))
	logger.debug("headers : {} ".format(headers))

	conn.request("POST", "/oauth/token", payload, headers)
	res = conn.getresponse()
	data = res.read()
	data = data.decode("utf-8")
	data = json.loads(data)

	# print (data)
	return data


# https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
def export_user(self, auth0_certificate, this_user):
	logger.debug("auth0_certificate\n{}\n".format(auth0_certificate))
	logger.debug("auth0_certificate - access-token\n{}\n".format(auth0_certificate['access_token']))

	headers = {'authorization': '{}'.format(auth0_certificate)}
	logger.debug("headers --\n{}\n--".format(headers))
	# conn = http.client.HTTPSConnection("realplayserver.dce1.humanify.com")
	# conn = http.client.HTTPSConnection("realplayserver.dce1.humanify.com")
	conn = http.client.HTTPSConnection("ttec-ped-developers.auth0.com")

	#  these sort of work , but stop at a 'redirect' message
	# conn.request("GET", "/tenants", headers=headers)
	conn.request("GET", "/users/"+ this_user, headers=headers)
	#bodyparam = "{123}"
	## conn.request("POST", "/api/v2/jobs/users-exports", headers=headers, json=bodyparam)
	#conn.request("POST", "/jobs/users-exports", headers=headers)

	res = conn.getresponse()
	data = res.read()
	logger.debug(data)


def get_auth0_certificate(client_domain_param, protocol="https"):
	# for now just make dummy data from milli-seconds
	logger.debug("\t\tI would call auth0 and pass :{} :: {}".format(client_domain_param, protocol))
	return step1_get_auth0_certificate(client_domain_param, protocol)
	#milli_date = datetime.utcnow().strftime('%A%d-%H:%M.%f')
	#logger.debug("\treturning milli date : {} ".format(milli_date))

	#return str(milli_date)


def get_auth0_role_data(client_domain_param, user_name):
	# for now just make dummy data from milli-seconds
	logger.debug("\t\tI would call auth0 and pass :{} :: {}".format(client_domain_param, user_name))
	milli_date = datetime.utcnow().strftime('%A%d-%H:%M.%f')
	logger.debug("\treturning milli date : {} ".format(milli_date))

	return str(milli_date)


def process_this_df(this_df, upload_filename, client_domain_param):
	auth0_certificate = get_auth0_certificate(client_domain_param)

	if 'access_token' not in auth0_certificate:
		logger.error('client : {} - auth0_cert :: {}\n'.format(client_domain_param,auth0_certificate))
		return
	logger.debug('client : {} - auth0_cert :: {}'.format(client_domain_param, auth0_certificate))
	logger.info('client : {} - auth0_cert :: {}'.format(client_domain_param, auth0_certificate))
	
	with open(upload_filename, 'w') as file_out:
		for index, row in this_df.iterrows():
			new_role = get_auth0_role_data(client_domain_param,row['user_id'])
			logging.info("domain {} - writing {} :{},{},{}".format(client_domain_param, upload_filename, row['user_id'], row['email'], new_role))
			file_out.write('\n{},{},{}'.format(row['user_id'], row['email'], new_role))

			# for debugging I just want 1 row
			break


def walklevel(some_dir, level=1):
	some_dir = some_dir.rstrip(os.path.sep)
	assert os.path.isdir(some_dir)
	num_sep = some_dir.count(os.path.sep)
	for root, dirs, files in os.walk(some_dir):
		yield root, dirs, files
		num_sep_this = root.count(os.path.sep)
		if num_sep + level <= num_sep_this:
			del dirs[:]


def process_input_files(json_or_csv="csv"):
	# Getting the work directory (cwd)
	source_dir = parser.get('user-export-file', 'source')

	output_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
	output_dir.mkdir(parents=True, exist_ok=True)

	src_extension = ".{}".format(json_or_csv)

	# r=root, d=directories, f = files
	for r, d, f in walklevel(source_dir, 0):
		for file in f:
			if file.endswith(src_extension):
				full_path = os.path.join(r, file)
				file_root = os.path.splitext(file)[0]
				# upload_filename = ("{}/{}{}{}".format(output_dir, 'output_', file_root, '.csv'))
				upload_filename = (
					"{}/{}{}{}".format(output_dir, parser.get('user-export-file', 'output_prefix'), file_root, '.csv'))

				logger.debug('\tfull_path          : {}'.format(full_path))
				logger.debug('\tsource_dir         : {}'.format(source_dir))
				logger.debug('\tfile_root          : {}'.format(file_root))
				logger.debug('\tupload_filename    : {}'.format(upload_filename))
				logger.debug('\toutput_dir         : {}'.format(output_dir))

				if (src_extension == '.json'):
					this_df = pd.read_json(full_path, lines=True)
				if (src_extension == '.csv'):
					this_df = pd.read_csv(full_path)

				#logger.debug(this_df.info)
				logger.debug(this_df.style)

				# we now have a dataframe for this file
				#  loop over the rows - make a call to auth0/users to get the roles
				#  write the user_id,email, roles to a new file : $file_root + 'processed' + .json
				process_this_df(this_df, upload_filename, file_root)


# def connect_to_db(postgres_hostname,postgres_ip,postgres_port,postgres_host,postgres_db_name,postgres_user,postgres_pswd):
def connect_to_db(postgres_hostname, postgres_port, postgres_host, postgres_db_name, postgres_user,
                  postgres_pswd):
	logger.debug("establishing the db connection to: {}".format(postgres_hostname))
	# establishing the connection
	conn = psycopg2.connect(
		database=postgres_db_name
		, user=postgres_user
		, password=postgres_pswd
		, host=postgres_host
		, port=postgres_port
	)
	logger.debug("connected to a db")
	return conn


def run_a_db_query(db_conn, my_stmt):
	cur = db_conn.cursor()
	cur.execute(my_stmt)
	items = cur.fetchall()
	return items
	# logger.debug(items)


def load_env_db_info(db_settings, environment='DEV_DB'):
	db_settings['postgres_hostname'] = parser.get(environment, 'hostname', fallback=" ")
	# db_settings['postgres_ip'] = parser.get(environment, 'private ip', fallback=" ")
	db_settings['postgres_port'] = parser.get(environment, 'port', fallback=" ")
	db_settings['postgres_host'] = parser.get(environment, 'host', fallback=" ")
	db_settings['postgres_db_name'] = parser.get(environment, 'db_name', fallback=" ")
	db_settings['postgres_user'] = parser.get(environment, 'user', fallback=" ")
	db_settings['postgres_pswd'] = parser.get(environment, 'pswd', fallback=" ")


def process_upload_files():
	logger.debug('Begin')

	# upload_source_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
	upload_source_dir = parser.get('user-export-file', 'output')
	logger.debug(upload_source_dir)

	postgres_envs = parser.get('Postgres_DBs', 'db_list').split(',')
	logger.debug('postgres_d : {}'.format(postgres_envs))

	db_settings = {}
	db_settings['postgres_hostname'] = " "
	# db_settings['postgres_ip'] = " "
	db_settings['postgres_port'] = " "
	db_settings['postgres_host'] = " "
	db_settings['postgres_db_name'] = " "
	db_settings['postgres_user'] = " "
	db_settings['postgres_pswd'] = " "

	for environment in parser.get('Postgres_DBs', 'db_list').split(','):
		logger.debug('processing env : {}'.format(environment))
		if (environment.lower() == 'dev'):
			logger.debug('found DEV env : {}'.format(environment))
			db_settings = load_env_db_info(db_settings, 'DEV_DB')
			#postgres_hostname = parser.get('DEV_DB', 'hostname', fallback=" ")
			## postgres_ip = parser.get('DEV_DB', 'private ip', fallback=" ")
			#postgres_port = parser.get('DEV_DB', 'port', fallback=" ")
			#postgres_host = parser.get('DEV_DB', 'host', fallback=" ")
			#postgres_db_name = parser.get('DEV_DB', 'db_name', fallback=" ")
			#postgres_user = parser.get('DEV_DB', 'user', fallback=" ")
			#postgres_pswd = parser.get('DEV_DB', 'pswd', fallback=" ")

		elif (environment.lower() == 'qa'):
			logger.debug('found QA env : {}'.format(environment))
			load_env_db_info('QA_DB')
			#postgres_hostname = parser.get('QA_DB', 'hostname', fallback=" ")
			## postgres_ip = parser.get('QA_DB', 'private ip', fallback=" ")
			#postgres_port = parser.get('QA_DB', 'port', fallback=" ")
			#postgres_host = parser.get('QA_DB', 'host', fallback=" ")
			#postgres_db_name = parser.get('QA_DB', 'db_name', fallback=" ")
			#postgres_user = parser.get('QA_DB', 'user', fallback=" ")
			#postgres_pswd = parser.get('QA_DB', 'pswd', fallback=" ")

		elif (environment.lower() == 'prod'):
			logger.debug('found PROD env : {}'.format(environment))
			load_env_db_info('PROD_DB')
			#postgres_hostname = parser.get('PROD_DB', 'hostname', fallback=" ")
			## postgres_ip = parser.get('PROD_DB', 'private ip', fallback=" ")
			#postgres_port = parser.get('PROD_DB', 'port', fallback=" ")
			#postgres_host = parser.get('PROD_DB', 'host', fallback=" ")
			#postgres_db_name = parser.get('PROD_DB', 'db_name', fallback=" ")
			#postgres_user = parser.get('PROD_DB', 'user', fallback=" ")
			#postgres_pswd = parser.get('PROD_DB', 'pswd', fallback=" ")

		if (db_settings['postgres_user'] == " "):
			logger.error('postgres database info not found - exiting')
			# exit(5)  # just made up a number
			break

	db_conn = connect_to_db(
		db_settings['postgres_hostname'],
		# db_settings['postgres_ip'],
		db_settings['postgres_port'],
		db_settings['postgres_host'],
		db_settings['postgres_db_name'],
		db_settings['postgres_user'],
		db_settings['postgres_pswd']
	)

	cur = db_conn.cursor()
	my_stmt = "select current_database();"
	cur.execute(my_stmt)
	items = cur.fetchall()
	logger.debug(items)

	# my_stmt = "ALTER USER {} WITH SUPERUSER;".format(postgres_user)
	my_stmt = "SELECT usename AS role_name, CASE WHEN usesuper AND usecreatedb THEN CAST('superuser, create database' AS pg_catalog.text) WHEN usesuper THEN CAST('superuser' AS pg_catalog.text) WHEN usecreatedb THEN CAST('create database' AS pg_catalog.text) ELSE CAST('' AS pg_catalog.text) END role_attributes FROM pg_catalog.pg_user ORDER BY role_name desc;"
	logger.debug(my_stmt)
	cur.execute(my_stmt)
	items = cur.fetchall()
	logger.debug(items)

	#  https://www.oodlestechnologies.com/blogs/Postgres-Sql-Update-Record-in-Bulk-from-CSV-file/

	# r=root, d=directories, f = files
	for r, d, f in walklevel(upload_source_dir, 0):
		for file in f:

			if file.endswith('.csv'):
				full_path = os.path.join(r, file)

				logger.debug('upload file:\n\t{}\n\tto {}'.format(full_path, postgres_db_name))
				my_stmt = "create temporary table gjs_test (user_id character varying(255) , email character varying(255) , roles character varying(255) );"
				# cur.execute(my_stmt)

				# this should work IF you get a superuser if
				my_stmt = "COPY gjs_test FROM '{}' WITH (FORMAT csv);".format(full_path)
				logger.debug("\t\t running this stmt\n{}".format(my_stmt))
				# cur.execute(my_stmt)

				# once that loads, run something like this to update from the new temp table:
				# UPDATE original_table SET original_table.dob = temp_table.dob FROM temp_table  Where original_table.id = temp_table.id;

				my_stmt = "select * from gjs_test;"
				# cur.execute(my_stmt)
				# items = cur.fetchall()
				# logger.debug(items)

				my_stmt = "drop table gjs_test;"
				# cur.execute(my_stmt)


def gjs_junk_holeder():
	logger.debug('just stuff')
	'''
	my_stmt = "create temporary table gjs_test (user_id character varying(255) , email character varying(255) , roles character varying(255) );"
	cur.execute(my_stmt)

	my_stmt = "copy public.gjs_test <filename> delimiter ',' csv noheader>;"
	cur.execute(my_stmt)

	my_stmt = "select * from gjs_test;"
	cur.execute(my_stmt)
	items = cur.fetchall()
	logger.debug(items)
	'''

	# my_stmt = "create temporary table gjs_test as select * from realplay_user;"
	# my_stmt = "create table public.gjs_test (user_id character varying(255) , email character varying(255) , roles character varying(255) );"
	###my_stmt = "create  table public.gjs_realplay_user as select * from realplay_user;"
	###cur.execute(my_stmt)

	# my_stmt = "select * from  gjs_realplay_user;"
	# cur.execute(my_stmt)
	# items = cur.fetchall()
	# logger.debug(items)

	# my_stmt = "create  table public.gjs_test as select realplay_user.userid , realplay_user.email , realplay_user.tenant from realplay_user;"
	# cur.execute(my_stmt)

	# my_stmt = "select * from  gjs_test;"
	# cur.execute(my_stmt)
	# items = cur.fetchall()
	# logger.debug(items)

	##my_stmt = "select nspname from pg_namespace where oid  =  pg_my_temp_schema();"
	##cur.execute(my_stmt)
	##items = cur.fetchall()
	##logger.debug(items)

	# my_stmt = "drop table gjs_test;"
	# cur.execute(my_stmt)

	# my_stmt = "select * from  gjs_test;"
	# cur.execute(my_stmt)
	# items = cur.fetchall()
	# logger.debug(items)


if __name__ == '__main__':
	parser = configparser.ConfigParser()
	logger = logging.getLogger("RealplayExportProcess")

	#log_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
	log_dir = Path("logs")
	log_dir.mkdir(parents=True, exist_ok=True)

	create_app()
	logger.debug(' start ')

	# test_log_messages()

	### either 'json' or 'csv'
	##process_input_files('json')
	process_input_files('csv')

	#process_upload_files()
