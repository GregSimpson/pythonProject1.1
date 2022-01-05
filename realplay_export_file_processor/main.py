##  install requirements from requirements.txt
# pip install -r requirements.txt

import configparser
import csv
import pprint
from datetime import datetime
from time import sleep, perf_counter

# pip install flask
from flask import Flask
import http
import json
import logging.config
import os
import pandas as pd
from pathlib import Path

# open a terminal 'at the bottom of intellij'
# pip install psycopg2-binary
import psycopg2
# pip install pyyaml
import yaml


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
	setup_logging()
	load_settings()

	return app


def call_auth0_to_get_certificate(client_domain_param, protocol="https"):
	call_auth0_to_get_certificate_timer_start = perf_counter()

	logger.debug("client_domain_param: {} :: protocol: {}".format(client_domain_param, protocol))

	# management API access token
	headers = {'content-type': "application/json"}
	# conn_str = "{}.auth0.com".format(client_domain_param)
	conn_str = parser.get(client_domain_param, 'client_domain')

	# gjs
	conn_api = "/oauth/token"
	payload = "{\"client_id\":\"" + parser.get(client_domain_param, 'client_id') + \
	          "\",\"client_secret\":\"" + parser.get(client_domain_param, 'client_secret') + \
	          "\",\"audience\":\"" + protocol + "://" + \
	          parser.get(client_domain_param, 'client_domain') + \
	          parser.get('Auth0Info', 'url_get_token')

	logger.info("headers --\n{}\n--".format(headers))
	logger.info("conn_str : {}".format(conn_str))
	logger.info("conn_api : {}".format(conn_api))
	logger.info("payload  : {}".format(payload))

	logger.debug("headers --\n{}\n--".format(headers))
	logger.debug("conn_str : {}".format(conn_str))
	logger.debug("conn_api : {}".format(conn_api))
	logger.debug("payload  : {}".format(payload))

	conn = http.client.HTTPSConnection(conn_str)

	conn.request("POST", conn_api, payload, headers)
	res = conn.getresponse()
	# TODO 
	#  check result list for 'error' and handle that
	# maybe - if (data['statusCode'] != 200):

	data = res.read()
	data = data.decode("utf-8")
	data = json.loads(data)
	conn.close()

	call_auth0_to_get_certificate_timer_stop = perf_counter()
	timer_results(client_domain_param, "call_auth0_to_get_certificate_timer", call_auth0_to_get_certificate_timer_start,
	              call_auth0_to_get_certificate_timer_stop)

	return data


# https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
def call_auth0_to_get_role_data(auth0_certificate, client_domain_param, user_name):
	call_auth0_to_get_role_data_timer_start = perf_counter()
	logger.debug(" seeking {} :: {}".format(client_domain_param, user_name))

	headers = {'authorization': 'Bearer {}'.format(auth0_certificate['access_token'])}
	conn_str = "{}.auth0.com".format(client_domain_param)
	conn_api = "/api/v2/users/{}/roles".format(user_name)
	conn = http.client.HTTPSConnection(conn_str)

	logger.debug("headers --\n{}\n--".format(headers))
	logger.debug("conn_str : {}".format(conn_str))
	logger.debug("conn_api : {}".format(conn_api))

	try:
		conn.request("GET", conn_api, headers=headers)
		res = conn.getresponse()
		data = res.read()
		logger.debug(type(data))
		logger.debug(data)

		data_as_json = json.loads(data.decode('utf-8'))
		data_pretty_printed = json.dumps(data_as_json, indent=2, sort_keys=True)

		#  check result list for 'error'
		if 'error' in data_as_json:
			raise Exception(data)

	except Exception as error:
		logging.error(data)
		return '{}'

	call_auth0_to_get_role_data_timer_stop = perf_counter()
	timer_results(client_domain_param, "call_auth0_to_get_role_data_timer", call_auth0_to_get_role_data_timer_start,
	              call_auth0_to_get_role_data_timer_stop)

	logger.debug(data_pretty_printed)
	return data_pretty_printed


def process_this_df(this_df, upload_filename, client_domain_param):
	process_this_df_timer_start = perf_counter()
	auth0_certificate = call_auth0_to_get_certificate(client_domain_param)

	if 'access_token' not in auth0_certificate:
		logger.error('client : {} - auth0_cert :: {}\n'.format(client_domain_param, auth0_certificate))
		return
	logger.debug('client : {} - auth0_cert :: {}'.format(client_domain_param, auth0_certificate))
	logger.info('client : {} - auth0_cert :: {}'.format(client_domain_param, auth0_certificate))

	# TODO
	#  check result of 'open'
	# maybe - raise exception

	# need this format to specify a delimiter
	with open(upload_filename, 'w') as file_out:
		writer = csv.writer(file_out, delimiter="!")

		total_counter = 0
		user_counter = 0
		number_of_sleeps = 0
		throttle_counter = (int)(parser.get('Config_Data', 'throttle_counter', fallback="10"))
		throttle_sleep = (int)(parser.get('Config_Data', 'throttle_sleep', fallback="30"))
		file_line_count = this_df.shape[0]

		for index, row in this_df.iterrows():

			if user_counter >= throttle_counter:
				number_of_sleeps += 1
				log_this_msg = 'Processed {} users; {} total out of {} \n\tSleeping for {} seconds\t\tThis is #{}\n'.format(
					throttle_counter, total_counter, file_line_count, throttle_sleep, number_of_sleeps)
				logger.debug(log_this_msg)
				logger.info(log_this_msg)

				sleep(throttle_sleep)
				user_counter = 0
			total_counter += 1
			user_counter += 1

			try:
				parsed_roles = json.loads(
					call_auth0_to_get_role_data(auth0_certificate, client_domain_param, row['user_id']))
				logger.debug("parsed_roles = {}".format(parsed_roles))
				if parsed_roles == {}:
					logger.error(" there was a problem getting the auth certificate")
					break

				role_str = ""
				for i in range(len(parsed_roles)):
					role_str = "{}{}".format(role_str, parsed_roles[i]['name'])
					if i < len(parsed_roles) - 1:
						role_str = "{},".format(role_str)
				##logger.debug("--{}--\n".format(parsed_roles[i]))
				# logger.debug("--{}--\n".format(parsed_roles[i]['name']))

				logging.info("domain {} - writing {} :{},{},{}".format(
					client_domain_param, upload_filename, row['user_id'], row['email'], role_str))
				writer.writerow([row['user_id'], row['email'], role_str])
			except Exception as error:
				logger.error(error)
				break

		log_this_msg = '\n\nProcessed {} users\tslept every {} \tseconds for {} seconds\t {} times\n'.format(
			total_counter, throttle_counter, throttle_sleep, number_of_sleeps)
		logger.debug(log_this_msg)
		logger.info(log_this_msg)

		process_this_df_timer_stop = perf_counter()
		timer_results(client_domain_param, "process_this_df_timer", process_this_df_timer_start,
		              process_this_df_timer_stop)


def walk_level(some_dir, level=1):
	some_dir = some_dir.rstrip(os.path.sep)
	assert os.path.isdir(some_dir)
	num_sep = some_dir.count(os.path.sep)
	for root, dirs, files in os.walk(some_dir):
		yield root, dirs, files
		num_sep_this = root.count(os.path.sep)
		if num_sep + level <= num_sep_this:
			del dirs[:]


def generate_upload_files_from_auth0_exports(json_or_csv="csv"):
	generate_upload_files_from_auth0_exports_timer_start = perf_counter()

	# Getting the work directory (cwd)
	source_dir = parser.get('user-export-file', 'source')

	output_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
	output_dir.mkdir(parents=True, exist_ok=True)

	# TODO
	#  clean this up to accept leading '.' or no '.'
	src_extension = ".{}".format(json_or_csv)

	# r=root, d=directories, f = files
	for r, d, f in walk_level(source_dir, 0):
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

				logger.info('\tNEW INPUT FILE     : {}'.format(full_path))
				logger.info('\tfull_path          : {}'.format(full_path))
				logger.info('\tsource_dir         : {}'.format(source_dir))
				logger.info('\tfile_root          : {}'.format(file_root))
				logger.info('\tupload_filename    : {}'.format(upload_filename))
				logger.info('\toutput_dir         : {}'.format(output_dir))

				if (src_extension == '.json'):
					this_df = pd.read_json(full_path, lines=True)
				if (src_extension == '.csv'):
					this_df = pd.read_csv(full_path)

				# logger.debug(this_df.info)
				logger.debug(this_df.style)

				# we now have a dataframe for this file
				#  loop over the rows - make a call to auth0/users to get the roles
				#  write the user_id,email, roles to a new file : $file_root + 'processed' + .json
				process_this_df(this_df, upload_filename, file_root)

	generate_upload_files_from_auth0_exports_timer_stop = perf_counter()
	timer_results("file-finding", "generate_upload_files_from_auth0_exports_timer"
	              , generate_upload_files_from_auth0_exports_timer_start
	              , generate_upload_files_from_auth0_exports_timer_stop)


def connect_to_db(postgres_hostname, postgres_port, postgres_host, postgres_db_name, postgres_user, postgres_pswd):
	connect_to_db_timer_start = perf_counter()

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
	# TODO
	#  check for success or failure

	connect_to_db_timer_stop = perf_counter()
	timer_results("", "connect_to_db_timer", connect_to_db_timer_start, connect_to_db_timer_stop)
	return conn


def run_a_db_query(db_conn, my_stmt):
	run_a_db_query_timer_start = perf_counter()

	cur = db_conn.cursor()
	cur.execute(my_stmt)
	items = cur.fetchall()

	run_a_db_query_timer_stop = perf_counter()
	timer_results("", "run_a_db_query_timer", run_a_db_query_timer_start, run_a_db_query_timer_stop)

	return items


def load_env_db_info(db_settings, environment='DEV_DB'):
	db_settings['postgres_hostname'] = parser.get(environment, 'hostname', fallback=" ")
	# db_settings['postgres_ip'] = parser.get(environment, 'private ip', fallback=" ")
	db_settings['postgres_port'] = parser.get(environment, 'port', fallback=" ")
	db_settings['postgres_host'] = parser.get(environment, 'host', fallback=" ")
	db_settings['postgres_db_name'] = parser.get(environment, 'db_name', fallback=" ")
	db_settings['postgres_user'] = parser.get(environment, 'user', fallback=" ")
	db_settings['postgres_pswd'] = parser.get(environment, 'pswd', fallback=" ")


def process_upload_files():
	process_upload_files_timer_method_start = perf_counter()

	# TODO
	#  see notes below
	upload_source_dir = parser.get('user-export-file', 'output')
	logger.debug(upload_source_dir)

	postgres_envs = parser.get('Postgres_DBs', 'db_list').split(',')
	logger.debug('postgres_d : {}'.format(postgres_envs))

	# TODO
	#  this might be removable TEST FIRST
	db_settings = {
		'postgres_hostname': " "
		, 'postgres_port': " "
		, 'postgres_host': " "
		, 'postgres_db_name': " "
		, 'postgres_user': " "
		, 'postgres_pswd': " "
	}
	# db_settings['postgres_ip'] = " "

	for environment in parser.get('Postgres_DBs', 'db_list').split(','):
		logger.debug('processing env : {}'.format(environment))

		if environment.lower() == 'local':
			logger.debug('found LOCAL env : {}'.format(environment))
			load_env_db_info(db_settings, 'LOCAL_DB')

		if environment.lower() == 'dev':
			logger.debug('found DEV env : {}'.format(environment))
			load_env_db_info(db_settings, 'DEV_DB')

		elif (environment.lower() == 'qa'):
			logger.debug('found QA env : {}'.format(environment))
			load_env_db_info('QA_DB')

		elif (environment.lower() == 'prod'):
			logger.debug('found PROD env : {}'.format(environment))
			load_env_db_info('PROD_DB')

		if (db_settings['postgres_user'] == " "):
			logger.error('postgres database info not found - exiting')
			# exit(5)  # just made up a number
			break

	# TODO
	#  check that the connect worked
	db_conn = connect_to_db(
		db_settings['postgres_hostname'],
		# db_settings['postgres_ip'],
		db_settings['postgres_port'],
		db_settings['postgres_host'],
		db_settings['postgres_db_name'],
		db_settings['postgres_user'],
		db_settings['postgres_pswd']
	)

	# TODO
	#  need privs to create temp table
	#  upload files to the temp table
	#  update realplay_user ROLES column from temp table
	#  where temp_table.userid = realplay_user.userid
	# r=root, d=directories, f = files
	for r, d, f in walk_level(upload_source_dir, 0):
		for file in f:
			if file.endswith('.csv'):
				full_path = os.path.join(r, file)
				logger.debug("\n\nPROCESSING file {}\n\n".format(full_path))

				try:

					cur = db_conn.cursor()
					# connection and db name test
					my_stmt = "select current_database();"
					cur.execute(my_stmt)
					items = cur.fetchall()
					logger.debug(items)

					role_upload_table = 'role_upload_table'
					logger.debug(
						'upload file:\n\t{} to db::{}  table::{}'.format(full_path, db_settings['postgres_db_name'],
						                                                 role_upload_table))

					# --- new query
					my_stmt = "create temporary table {} (userid character varying(255) , email character varying(255) , auth0_roles character varying(255) );".format(
						role_upload_table)
					logger.debug(my_stmt)
					cur.execute(my_stmt)

					# --- new query
					#  upload csv file to temp table
					with open(full_path, 'r') as f:
						next(f)
						cur.copy_from(f, role_upload_table, sep='!')
					db_conn.commit()
					f.close()

					target_realplay_user_table = "realplay_user"
					my_stmt = "update {} set \
						auth0_roles = {}.auth0_roles \
						, email = {}.email \
						from {} \
						where {}.userid = {}.userid \
						and {}.auth0_roles <> {}.auth0_roles \
						 ".format(target_realplay_user_table, role_upload_table, role_upload_table, role_upload_table,
					              target_realplay_user_table, role_upload_table, target_realplay_user_table,
					              role_upload_table)

					logger.debug(my_stmt)
					cur.execute(my_stmt)

					logger.debug("AFTER the update\n\n\n")
					# --- new query
					#  show the target_realplay_user_table
					my_stmt = "SELECT userid, email, auth0_roles FROM {} where email = 'greg.simpson@ttec.com' order by  auth0_roles asc ;".format(
						target_realplay_user_table)
					logger.debug(my_stmt)
					cur.execute(my_stmt)
					row = cur.fetchone()

					while row is not None:
						logger.debug(row)
						row = cur.fetchone()

					# --- new query
					#  show the target_realplay_user_table
					my_stmt = "SELECT DISTINCT auth0_roles FROM {};".format(target_realplay_user_table)
					logger.debug(my_stmt)
					cur.execute(my_stmt)
					row = cur.fetchone()

					while row is not None:
						logger.debug(row)
						row = cur.fetchone()

					# --- new query
					#  show final table values
					my_stmt = "SELECT count(*) from {} a , {} b where a.userid = b.userid".format(
						target_realplay_user_table, role_upload_table)
					logger.debug(my_stmt)
					cur.execute(my_stmt)
					row = cur.fetchone()

					while row is not None:
						logger.debug(row)
						row = cur.fetchone()

					# --- new query
					#  commit
					my_stmt = "commit"
					logger.debug(my_stmt)
					cur.execute(my_stmt)

				except (Exception, psycopg2.DatabaseError) as error:
					logger.error(error)
				finally:
					if db_conn is not None:
						# --- new query
						my_stmt = "drop table if exists {} ".format(role_upload_table)
						logger.debug(my_stmt)
						cur.execute(my_stmt)
						cur.close()

	db_conn.close()

	process_upload_files_timer_method_stop = perf_counter()
	timer_results("", "process_upload_files_timer_method_", process_upload_files_timer_method_start,
	              process_upload_files_timer_method_stop)


def timer_results(client_domain_param, timer_name, timer_start, timer_stop):
	key_name = ("{}_{}".format(client_domain_param, timer_name))
	# timer_dict[key_name] = timer_start - timer_stop
	# timer_dict[key_name] = "{} seconds".format((timer_stop - timer_start)/1000)
	timer_dict[key_name] = "{}".format((timer_stop - timer_start) / 1000)

# does not seem to include sleep - it should
# https://www.reddit.com/r/learnpython/comments/bjjafq/for_performance_timing_what_time_do_i_use/


def display_timer_results():
	# logger.debug("\ntimer_dict : {}\n".format(timer_dict))
	# Prints the nicely formatted dictionary
	logger.info(" Time is in seconds ")
	logger.info(pprint.pprint(timer_dict))
	logger.info("\n\n ")
	pprint.pprint(timer_dict)


if __name__ == '__main__':
	parser = configparser.ConfigParser()
	logger = logging.getLogger("RealplayExportProcess")

	# tried dynamically - did not spend time to make it work
	# log_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
	log_dir = Path("logs")
	log_dir.mkdir(parents=True, exist_ok=True)

	create_app()
	logger.debug('BEGIN process')

	# test_log_messages()

	timer_dict = {}
	whole_process_timer_start = perf_counter()

	# STEP 1 add role info to the file to be uploaded
	### can be either 'json' or 'csv'
	##generate_upload_files_from_auth0_exports('json')
	generate_upload_files_from_auth0_exports('csv')

	# STEP 2 upload the file and update realplay_user where the userids match
	process_upload_files()

	whole_process_timer_stop = perf_counter()

	timer_results("main", "whole_process_timer", whole_process_timer_start, whole_process_timer_stop)
	display_timer_results()

	logger.debug('END process')
