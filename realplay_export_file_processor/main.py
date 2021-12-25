import configparser
import csv
import pprint
from datetime import datetime
from time import sleep, perf_counter

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
	###client_domain_param + call_auth0_to_get_certificate_timer_start = perf_counter()
	logger.debug("client_domain_param: {} :: protocol: {}".format(client_domain_param, protocol))

	# management API access token
	headers = {'content-type': "application/json"}
	conn_str = "{}.auth0.com".format(client_domain_param)
	conn_api = "/oauth/token"
	payload = "{\"client_id\":\"" + parser.get(
		client_domain_param,'client_id') + "\",\"client_secret\":\"" + parser.get(
		client_domain_param, 'client_secret') + "\",\"audience\":\"" + protocol + "://" + parser.get(
		client_domain_param, 'client_domain') + parser.get('Auth0Info', 'url_get_token')

	conn = http.client.HTTPSConnection(conn_str)

	logger.debug("headers --\n{}\n--".format(headers))
	logger.debug("conn_str : {}".format(conn_str))
	logger.debug("conn_api : {}".format(conn_api))

	conn.request("POST", conn_api, payload, headers)
	res = conn.getresponse()
	# TODO 
	#  check result list for 'error' and handle that
	# maybe - if (data['statusCode'] != 200):

	data = res.read()
	data = data.decode("utf-8")
	data = json.loads(data)

	call_auth0_to_get_certificate_timer_stop = perf_counter()
	timer_results("call_auth0_to_get_certificate_timer", call_auth0_to_get_certificate_timer_start,
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

	conn.request("GET", conn_api, headers=headers)
	res = conn.getresponse()
	# TODO 
	#  check result list for 'error' and handle that
	# maybe - if (data['statusCode'] != 200):

	data = res.read()
	logger.debug(type(data))
	logger.debug(data)

	data_as_json = json.loads(data.decode('utf-8'))
	data_pretty_printed = json.dumps(data_as_json, indent=2, sort_keys=True)
	logger.debug(data_pretty_printed)

	call_auth0_to_get_role_data_timer_stop = perf_counter()
	timer_results("call_auth0_to_get_role_data_timer", call_auth0_to_get_role_data_timer_start,
	              call_auth0_to_get_role_data_timer_stop)

	return data_pretty_printed


def process_this_df(this_df, upload_filename, client_domain_param):
	process_this_df_timer_start = perf_counter()
	auth0_certificate = call_auth0_to_get_certificate(client_domain_param)

	if 'access_token' not in auth0_certificate:
		logger.error('client : {} - auth0_cert :: {}\n'.format(client_domain_param, auth0_certificate))
		return
	logger.debug('client : {} - auth0_cert :: {}'.format(client_domain_param, auth0_certificate))
	logger.info('client : {} - auth0_cert :: {}'.format(client_domain_param, auth0_certificate))

	# with open(upload_filename, 'w') as file_out:
	#	for index, row in this_df.iterrows():
	#		new_role = get_auth0_role_data(auth0_certificate,client_domain_param,row['user_id'])
	#		logging.info("domain {} - writing {} :{},{},{}".format(client_domain_param, upload_filename, row['user_id'], row['email'], new_role))
	#		file_out.write('\n{},{},{}'.format(row['user_id'], row['email'], new_role))

	# TODO 
	#  check result of 'open'
        # maybe - raise exception

	with open(upload_filename, 'w') as file_out:
		writer = csv.writer(file_out, delimiter="!")

		user_counter = 0
		number_of_sleeps = 0
		throttle_counter = (int)(parser.get('Config_Data', 'throttle_counter', fallback="10"))
		throttle_sleep = (int)(parser.get('Config_Data', 'throttle_sleep', fallback="30"))

		for index, row in this_df.iterrows():
			user_counter += 1
			if user_counter > throttle_counter:
				number_of_sleeps += 1
				logger.debug('Processed {} users - Sleeping for {} seconds\t\tThis is #{}\n'.format(throttle_counter, throttle_sleep, number_of_sleeps))
				sleep(throttle_sleep)
				user_counter = 0

			new_role = call_auth0_to_get_role_data(auth0_certificate, client_domain_param, row['user_id'])
			logging.info("domain {} - writing {} :{},{},{}".format(
				client_domain_param, upload_filename, row['user_id'], row['email'], new_role))
			writer.writerow([row['user_id'], row['email'], new_role])

		logger.debug('\tSlept every {} users\t\tfor {} seconds\t\t{} times\n'.format(
			throttle_counter, throttle_sleep, number_of_sleeps))

		process_this_df_timer_stop = perf_counter()
		timer_results("process_this_df_timer", process_this_df_timer_start, process_this_df_timer_stop)


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
	timer_results("generate_upload_files_from_auth0_exports_timer"
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
	timer_results("connect_to_db_timer", connect_to_db_timer_start, connect_to_db_timer_stop)
	return conn


def run_a_db_query(db_conn, my_stmt):
	run_a_db_query_timer_start = perf_counter()

	cur = db_conn.cursor()
	cur.execute(my_stmt)
	items = cur.fetchall()

	run_a_db_query_timer_stop = perf_counter()
	timer_results("run_a_db_query_timer", run_a_db_query_timer_start, run_a_db_query_timer_stop)

	return items


def load_env_db_info(db_settings, environment='DEV_DB'):
	db_settings['postgres_hostname'] = parser.get(environment, 'hostname', fallback=" ")
	# db_settings['postgres_ip'] = parser.get(environment, 'private ip', fallback=" ")
	db_settings['postgres_port'] = parser.get(environment, 'port', fallback=" ")
	db_settings['postgres_host'] = parser.get(environment, 'host', fallback=" ")
	db_settings['postgres_db_name'] = parser.get(environment, 'db_name', fallback=" ")
	db_settings['postgres_user'] = parser.get(environment, 'user', fallback=" ")
	db_settings['postgres_pswd'] = parser.get(environment, 'pswd', fallback=" ")


def process_upload_files_incomplete_for_now():
	process_upload_files_incomplete_for_now_timer_start = perf_counter()

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
                # TODO
                #  add LOCAL env def
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

        # TODO
        #  work on this using a LOCAL db - then all you need are the right privs on the other envs

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

				logger.debug('upload file:\n\t{}\n\tto {}'.format(full_path, postgres_db_name))
				my_stmt = "create temporary table gjs_test (user_id character varying(255) , email character varying(255) , roles character varying(255) );"
				# cur.execute(my_stmt)

				# this should work IF you get a superuser if
				my_stmt = "COPY gjs_test FROM '{}' WITH (FORMAT csv);".format(full_path)
				logger.debug("\t\t running this stmt\n{}".format(my_stmt))
				# cur.execute(my_stmt)

				# once that loads, run something like this to update from the new temp table:
				# UPDATE original_table SET original_table.dob = temp_table.dob FROM temp_table
				#  Where original_table.id = temp_table.id;

				my_stmt = "select * from gjs_test;"
				# cur.execute(my_stmt)
				# items = cur.fetchall()
				# logger.debug(items)

				my_stmt = "drop table gjs_test;"
				# cur.execute(my_stmt)

	process_upload_files_incomplete_for_now_timer_stop = perf_counter()
	timer_results("process_upload_files_incomplete_for_now_timer", process_upload_files_incomplete_for_now_timer_start,
	              process_upload_files_incomplete_for_now_timer_stop)


def timer_results(timer_name, timer_start, timer_stop):
	#timer_dict[timer_name] = timer_start - timer_stop
	timer_dict[timer_name] = "{} seconds".format((timer_start - timer_stop)/1000)

	# does not seem to include sleep - it should
	# https://www.reddit.com/r/learnpython/comments/bjjafq/for_performance_timing_what_time_do_i_use/


def display_timer_results():
	#logger.debug("\ntimer_dict : {}\n".format(timer_dict))
	# Prints the nicely formatted dictionary
	pprint.pprint(timer_dict)


if __name__ == '__main__':
	parser = configparser.ConfigParser()
	logger = logging.getLogger("RealplayExportProcess")

	# log_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
	log_dir = Path("logs")
	log_dir.mkdir(parents=True, exist_ok=True)

	create_app()
	logger.debug('BEGIN process')

	# test_log_messages()

	timer_dict = {}
	whole_process_timer_start = perf_counter()
	generate_upload_files_timer_start = perf_counter()

	### either 'json' or 'csv'
	##generate_upload_files_from_auth0_exports('json')
	generate_upload_files_from_auth0_exports('csv')

	generate_upload_files_timer_stop = perf_counter()

	# process_upload_files_incomplete_for_now_timer_start = perf_counter()
	# process_upload_files_incomplete_for_now()
	# process_upload_files_incomplete_for_now_timer_stop = perf_counter()

	whole_process_timer_stop = perf_counter()

	timer_results("generate_upload_files_timer", generate_upload_files_timer_start, generate_upload_files_timer_stop)
	# timer_results("process_upload_files_incomplete_for_now_timer", process_upload_files_incomplete_for_now_timer_start, process_upload_files_incomplete_for_now_timer_stop)
	timer_results("whole_process_timer", whole_process_timer_start, whole_process_timer_stop)

	display_timer_results()

	logger.debug('END process')
