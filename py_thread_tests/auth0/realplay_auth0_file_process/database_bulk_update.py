##  install requirements from requirements.txt
# pip install -r requirements.txt

# NOTE bulk insert options
# https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/

import configparser
import http
import http.client
import io
import json
import logging.config
import os
import random
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from time import sleep, time



import pandas as pd
# https://www.postgresql.org/docs/current/errcodes-appendix.html#ERRCODES-TABLE
import psycopg2
import yaml
from psycopg2 import extras
# sudo apt-get install python3.10-distutils
# python3.10 -m pip install opencv-python

from timeout import timeout, TimeoutError

from sqlalchemy import create_engine
from sqlalchemy import text
from config_db import config_db_from_env
# read connection parameters
# params = config_db_from_ini()
params = config_db_from_env()

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class Auth0UserNotFoundException(Error):
    """Raised when the Auth0 user is not found"""
    pass


class MyTimeoutException(Error):
    """Raised when the Auth0 get user role api call times out"""
    pass


class BadDatabaseNameException(Error):
    """Raised when the specified database does not exist"""
    pass


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


#  read these env variables
# DB Info:
# Dev - POSTGRES_CONNECTION: '{
# "host":<hostname>
# "port":5432
# "user":"realplayuser"
# "password":<pswd>
# "database":"realplay_dce1"
# }'
# QA is all the same except for the database name

# https://stackoverflow.com/questions/40326540/how-to-assign-default-value-if-env-var-is-empty
#  os.getenv('MONGO_PASS', 'pass') where pass is the default value if MONGO_PASS env var isn't set

def load_settings_from_ini():
    # https://www.tutorialspoint.com/configuration-file-parser-in-python-configparser
    # parser = configparser.ConfigParser()
    parser.read('conf/settings.ini')
    for sect in parser.sections():
        logger.info('Section: {}'.format(sect))
        for k, v in parser.items(sect):
            if k not in ('client_id', 'client_secret', 'pswd'):
                logger.info(' {} = {}'.format(k, v))
            else:
                logger.info(' {} = {}'.format(k, 'hidden'))
        logger.info(' ')


def create_app():
    setup_logging()
    load_settings_from_ini()

    return


# this is used to simulate timeouts during debugging
def random_sleep(a=1, b=30):
    # selects a random value from the list
    list1 = [1, 2, 3, 4, 5]
    list2 = range(a, b)
    sleep_number = random.choice(list2)
    logger.debug("\t\tSleeping for {}".format(sleep_number))
    sleep(sleep_number)


# https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
@timeout(10)
def call_auth0_to_get_certificate(client_domain_param, protocol="https"):
    logger.debug("client_domain_param: {} :: protocol: {}".format(client_domain_param, protocol))
    data = None

    # management API access token
    headers = {'content-type': "application/json"}
    conn_str = parser.get(client_domain_param, 'client_domain')

    conn_api = "/oauth/token"
    payload = "{\"client_id\":\"" + \
              parser.get(client_domain_param, 'client_id') + \
              "\",\"client_secret\":\"" + \
              parser.get(client_domain_param, 'client_secret') + \
              "\",\"audience\":\"" + protocol + "://" + \
              parser.get(client_domain_param, 'client_domain') + \
              parser.get('Auth0Info', 'url_get_token')

    logger.info("\tconn_str : {}".format(conn_str))
    logger.info("\tconn_api : {}".format(conn_api))
    logger.debug("\theaders  : {}".format(headers))
    logger.debug("\tpayload  : {}\n\n".format("payload details hidden"))

    # TODO highlight
    ## NOTE - timeout simulator for debugging
    # random_sleep()

    try:
        logger.debug("Calling auth0 to get certificate\n")
        conn = http.client.HTTPSConnection(conn_str)

        conn.request("POST", conn_api, payload, headers)
        res = conn.getresponse()
        data = res.read()

        data_as_json = json.loads(data.decode('utf-8'))
        data_pretty_printed = json.dumps(data_as_json, indent=2, sort_keys=True)

        logger.debug(data_pretty_printed)
        conn.close()

        if 'error' in data_as_json:
            raise Exception(data)

        logger.debug("\n\n\t\tGood call to get certificate\n\n")

    # TODO handle new exception type ?  maybe
    except Exception as error:
        if data is None:
            logger.error(" problem happened before data is initialized ")
        else:
            logger.error(data)
        raise TimeoutError

    return data_as_json


# https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
@timeout(5)
def call_auth0_to_get_role_data(auth0_certificate, client_domain_param, user_name):
    logger.debug(
        "\tseeking tenant - {} :: userid - {}".format(parser.get(client_domain_param, 'client_domain'), user_name))

    headers = {'authorization': 'Bearer {}'.format(auth0_certificate['access_token'])}
    conn_str = parser.get(client_domain_param, 'client_domain')
    conn_api = "/api/v2/users/{}/roles".format(user_name)
    conn = http.client.HTTPSConnection(conn_str)

    logger.info("\tconn_str : {}".format(conn_str))
    logger.info("\tconn_api : {}".format(conn_api))
    logger.debug("\theaders  : {}".format(headers))

    # TODO highlight
    #  NOTE - timeout simulator for debugging
    # random_sleep()

    conn.request("GET", conn_api, headers=headers)
    res = conn.getresponse()
    data = res.read()

    data_as_json = json.loads(data.decode('utf-8'))
    data_pretty_printed = json.dumps(data_as_json, indent=2, sort_keys=True)
    logger.info(data_pretty_printed)

    #  check result list for 'error'
    if 'error' in data_as_json:
        raise Auth0UserNotFoundException(data)

    return data_pretty_printed


def log_this_summary_by_database(total_counter, total_to_be_done, throttle_counter,
                                 throttle_sleep, number_of_sleeps,
                                 processed_so_far, tenant_elapsed_time, timeout_counter, not_found_counter):

    tenant_elapsed_time = (time() - tenant_elapsed_time)
    overall_elapsed_time = (time() - overall_runtime_start)
    num_remaining_to_process = total_to_be_done - total_counter
    if processed_so_far == 0:
        avg_time_per_userid = 0
    else:
        avg_time_per_userid = (overall_elapsed_time / processed_so_far)
    estimated_time_remaining = str(timedelta(seconds=(num_remaining_to_process * avg_time_per_userid)))
    estimated_end_time = format_time_stamp(time() + (num_remaining_to_process * avg_time_per_userid), "%H:%M:%S")

    logger.debug('\n')
    logger.debug('\t\t avg_time_per_userid      : {}'.format(avg_time_per_userid))
    logger.debug('\t\t num_remaining_to_process : {}'.format(num_remaining_to_process))
    logger.debug('\t\t overall_runtime_start    : {}'.format(format_time_stamp(overall_runtime_start, "%H:%M:%S")))
    logger.debug('\t\t minutes_remaining        : {}'.format(
        format_time_stamp((num_remaining_to_process * avg_time_per_userid) / 60, "%M:%S:%m")))
    logger.debug('\t\t time() + sec_rem         : {}\n'.format(
        format_time_stamp(time() + (num_remaining_to_process * avg_time_per_userid), "%H:%M:%S")))

    # file process summary
    log_this_msg = '\n\n\tProcessed {} users total out of {} in database : {}' \
                   '\n\t\t\tsleeping every {} users for {} seconds {} times' \
                   '\n\t\t\t\tthis block time taken {}' \
                   '\n\tOverall time taken : {}' \
                   '\n\t\taverage time per user : {}' \
                   '\n\n\tEstimated_end_time       : {} (localtime)' \
                   '\n\t\tprocess started at       : {} (localtime)' \
                   '\n\t\testimated_time_remaining : {}  - gets more reliable as the process runs' \
                   '\n\n\tTimeouts encountered so far = {}' \
                   '\n\tNotFound encountered so far = {}' \
                   '\n\t\tsee the error log for details\n' \
        .format(total_counter,
                total_to_be_done,
                params['database'],
                throttle_counter,
                throttle_sleep,
                number_of_sleeps,
                str(timedelta(seconds=tenant_elapsed_time)),
                str(timedelta(seconds=overall_elapsed_time)),
                str(timedelta(seconds=avg_time_per_userid)),
                estimated_end_time,
                format_time_stamp(overall_runtime_start, "%H:%M:%S"),
                estimated_time_remaining,
                timeout_counter,
                not_found_counter)
    logger.info(log_this_msg)


def format_time_stamp(result, format_str="%H:%M:%S:%f"):
    output = datetime.strftime(datetime.fromtimestamp(result), format_str)
    return output


def populate_auth0_role_column_in_dataframe(this_df, processed_so_far, timeout_counter, not_found_counter):
    tenant_elapsed_time = time()

    total_counter = 0
    user_counter = 0
    number_of_sleeps = 0
    throttle_counter = int(parser.get('Config_Data', 'throttle_counter', fallback="10"))
    throttle_sleep = int(parser.get('Config_Data', 'throttle_sleep', fallback="30"))

    for index, row in this_df.iterrows():
        try:
            # TODO highlight
            ## NOTE - debug testing limit
            #if user_counter >= throttle_counter:
            #    return processed_so_far, timeout_counter, not_found_counter

            # this pattern works for all except ttec-ped-developers domain
            tenant_domain = "ttec-realplay-" + row['tenant']

            # TODO highlight
            #  NOTE - Auth0 get_certificate
            auth0_certificate = call_auth0_to_get_certificate(tenant_domain)

            logger.debug('client : {} - auth0_cert :: {}'.format(tenant_domain, auth0_certificate))
            if 'access_token' not in auth0_certificate:
                return

            if user_counter >= throttle_counter:
                # NOTE - just for debugging
                # if processed_so_far >= (10 * number_of_sleeps):
                # return processed_so_far, timeout_counter, not_found_counter
                # exit(66)
                # logger.debug("\n\n{}".format(this_df))
                # show_dataframe(this_df, 100)

                number_of_sleeps += 1
                log_this_summary_by_database(total_counter, len(this_df) - 1, throttle_counter, throttle_sleep,
                                             number_of_sleeps, processed_so_far, tenant_elapsed_time,
                                             timeout_counter, not_found_counter)
                sleep(throttle_sleep)
                user_counter = 0
                tenant_elapsed_time = time()

            total_counter += 1
            user_counter += 1
            processed_so_far += 1
            logger.debug('\n\n\tprocessed_so_far:{} - user_counter:{}'.format(processed_so_far, user_counter))

            parsed_roles = json.loads(
                # TODO highlight
                #  NOTE - Auth0 get_role_data
                call_auth0_to_get_role_data(auth0_certificate, tenant_domain, row['user_id']))
            logger.debug("parsed_roles = {}".format(parsed_roles))

            if parsed_roles == {}:
                logger.error(" there was a problem with the auth certificate")
                break

            role_str = ""
            for i in range(len(parsed_roles)):
                role_str = "{}{}".format(role_str, parsed_roles[i]['name'])
                if i < len(parsed_roles) - 1:
                    role_str = "{},".format(role_str)

            email_str = row['email'].replace("\'", "-")
            logger.info("domain {} - writing :{},{},{}".format(
                tenant_domain, row['user_id'], email_str, role_str))

            json_count = 0
            json_parts = role_str.split(',')
            json_str = '{'
            for each_role in json_parts:
                json_str = json_str + '"{}": "{}"'.format(json_count, each_role)
                json_count += 1
                if json_count < len(json_parts):
                    json_str = json_str + ', '
            json_str = '{}{}'.format(json_str, '}')
            logger.debug('\t' + json_str)
            json_str = json.dumps(json_str)
            logger.debug(json_str)

            # update the auth0_roles column of the df where user_id == '<whatever>'
            this_df.loc[this_df['user_id'] == row['user_id'], 'auth0_roles'] = json_str

            # save dataframe to disk
            this_df.to_pickle("saved_dataframe.pkl")
            # Then you can load it back using:
            # df = pd.read_pickle(file_name)

        except Auth0UserNotFoundException as error:
            logger.error("\tAuth0UserNotFoundException  {}".format(" incrementing not_found_counter"))
            not_found_counter += 1
            log_psycopg2_exception_info(error, tenant_domain, row['user_id'], error.args)

        except TimeoutError as error:
            # TODO add this user to the (NEW) redo list ???
            logger.error("\tTimeoutError  {}".format(" incrementing timeout_counter"))
            timeout_counter += 1
            if row['user_id'] is not None:
                log_psycopg2_exception_info(error, tenant_domain, row['user_id'], error.args)

        except Exception as error:
            logger.error("\tUnKnown Exception  {}".format(error))
            if row['user_id'] is not None:
                log_psycopg2_exception_info(error, tenant_domain, row['user_id'], error.args)

    # process summary
    log_this_summary_by_database(total_counter, len(this_df) - 1, throttle_counter, throttle_sleep,
                                 number_of_sleeps, processed_so_far, tenant_elapsed_time,
                                 timeout_counter, not_found_counter)

    return processed_so_far, timeout_counter, not_found_counter


def log_psycopg2_exception_info(error, tenant_domain, user_id, args):
    logger.error("\tclient_domain_param : {}".format(tenant_domain))
    logger.error("\trow[\'user_id\']      : {}".format(user_id))
    logger.error("\terror.args            : {}".format(args))
    logger.error("\ttype(error)           : {}\n\n".format(type(error)))


def db_connect_return_conn():
    """ Return connection to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        logger.debug('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("\tException  {}".format(error))

    return conn


def db_connect_return_cursor():
    """ Return connection to the PostgreSQL database server """
    conn = None
    try:
        conn = db_connect_return_conn()
        # create a cursor
        cur = conn.cursor()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("\tException  {}".format(error))

    return cur


def test_this_db_connection_by_cursor(cur):
    logger.debug('test_this_db_connection_by_cursor')
    try:
        # execute a statement
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        logger.debug('PostgreSQL database version: ' + str(db_version))

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def test_this_db_connection_by_conn(conn):
    logger.debug('test_this_db_connection_by_conn')
    try:
        this_df = pd.read_sql("""select version()""", conn)
        show_dataframe(this_df, 2)

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def show_dataframe(df, limit=20):
    role_counter = 1
    for index, row in df.iterrows():
        if role_counter <= limit:
            #if 'auth0_roles' in df:
            #if (row['auth0_roles'] != '""') and (len(row['auth0_roles']) > 16):
            logger.debug("\n{} {}".format(role_counter, row))
            logger.debug(" - - - - - - - ")
            role_counter += 1


# TODO the newest for db access
def get_userid_email_tenant_from_db_sqlalchemy(my_cursor):
    # https://www.compose.com/articles/using-postgresql-through-sqlalchemy/

    logger.debug("\tparams : {}\n\t\tvalues : {}".format(params.keys(), params.values()))

    logger.info("\tuser     : {}".format(params['user']))
    logger.info("\tpassword : {}".format(' <hidden> '))
    logger.info("\tport     : {}".format(params['port']))
    logger.info("\thost     : {}".format(params['host']))
    logger.info("\tdatabase : {}".format(params['database']))
    db_string = "postgresql://{}:{}@{}:{}/{}".format(params['user'], params['password'], params['host'], params['port'], params['database'])
    #logger.debug("db_string : \n{}".format(db_string))

    db_schema_version = os.getenv('db_schema_version')
    logger.info("\tdb_schema_version : {}".format(db_schema_version))

    engine = create_engine(db_string)

    #result_set = db.execute("select * from realplay_user")
    #for r in result_set:
    #    logger.debug(r)

    query_api_v1 = 'SELECT USERID AS user_id '\
                          ', EMAIL AS email'\
                          ', TENANT AS tenant'\
                          ' FROM REALPLAY_USER '\
                          ' WHERE ACTIVE = \'true\' '\
                          ' ORDER BY 3,2'

    query_api_v2 = 'SELECT rpu.auth0_user_id AS user_id '\
                          ', rpu.email AS email '\
                          ', t.tenant_name AS tenant '\
                          ' FROM realplay_user rpu '\
                          ' JOIN tenant t '\
                          ' ON rpu.tenant_id = t.tenant_id ' \
                          ' WHERE ACTIVE = \'true\' ' \
                          ' ORDER BY 3,2'

    sql = query_api_v1
    if db_schema_version == 'v2':
        sql = query_api_v2

    logger.debug("SQL str : \n\t{}".format(sql))
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql))
    dataframe = pd.DataFrame(query.fetchall())

    return dataframe




def update_dataframe_from_auth0(my_conn, userid_email_tenant_auth0_role_df):

    processed_so_far = 0
    timeout_counter = 0
    not_found_counter = 0

    # TODO gjs remove these ?
    processed_so_far, timeout_counter, not_found_counter = populate_auth0_role_column_in_dataframe(
                                                            userid_email_tenant_auth0_role_df,
                                                            processed_so_far,
                                                            timeout_counter,
                                                            not_found_counter)

    return userid_email_tenant_auth0_role_df


def drop_table(engine, temp_table_name='test_table_2'):
    sql = 'DROP TABLE IF EXISTS {};'.format(temp_table_name)
    logger.debug("SQL str : \n\t{}".format(sql))
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql))


def show_table_contents(engine, temp_table_name='test_table_2'):
    # https://towardsdatascience.com/how-to-convert-sql-query-results-to-a-pandas-dataframe-a50f0d920384
    sql = """SELECT * FROM {}""".format(temp_table_name)
    logger.debug("SQL str : \n\t{}".format(sql))
    #dataframe = pd.read_sql(sql, my_conn)

    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql))
    dataframe = pd.DataFrame(query.fetchall())

    show_dataframe(dataframe, 3)

    return dataframe


def write_dataframe_to_table(df, db_engine, schema, table_name, if_exists='replace'):
    logger.debug(" BEGIN  {} - {}".format("write_dataframe_to_table", table_name))

    string_data_io = io.StringIO()
    df.to_csv(string_data_io, sep='|', index=False)
    pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine, schema=schema)
    table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df,
                               index=False, if_exists='replace', schema=schema)
    table.create()
    string_data_io.seek(0)
    string_data_io.readline()  # remove header
    with db_engine.connect() as connection:
        with connection.connection.cursor() as cursor:
            copy_cmd = "COPY %s.%s FROM STDIN HEADER DELIMITER '|' CSV" % (schema, table_name)
            cursor.copy_expert(copy_cmd, string_data_io)
        connection.connection.commit()


def bulk_load_temp_table(df, page_size=100):
    logger.debug("BEGIN  {}".format("bulk_load_temp_table"))
    try:
        temp_table_name = 'test_table_2'

        db_string = "postgresql://{}:{}@{}:{}/{}".format(params['user'], params['password'], params['host'], params['port'], params['database'])
        engine = create_engine(db_string)

        write_dataframe_to_table(df, engine, 'public', temp_table_name, if_exists='replace')

        show_table_contents(engine, temp_table_name)

        update_realplay_user_table(engine, temp_table_name)

        show_table_contents(engine, temp_table_name)

        drop_table(engine, temp_table_name)

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error: %s" % error)
        return 1


def update_realplay_user_table(engine, temp_table_name):
    realplay_user_table = parser.get('Config_Data', 'realplay_user_table')

    # version test
    update_api_v1 = ' UPDATE {} SET auth0_roles = ' \
                           ' cast(TTN.auth0_roles AS JSON) FROM {} TTN '\
                           ' WHERE {}.userid = TTN.user_id ;'\
        .format(realplay_user_table, temp_table_name, realplay_user_table)

    update_api_v2 = ' UPDATE {} SET auth0_roles = ' \
                           ' cast(TTN.auth0_roles AS JSON) FROM {} TTN ' \
                           ' WHERE {}.auth0_user_id = TTN.user_id ;' \
        .format(realplay_user_table, temp_table_name, realplay_user_table)

    sql = update_api_v1
    if params['database'] == 'realplay2_dce1':
        sql = update_api_v2

    logger.debug("SQL str : \n\t{}".format(sql))
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql + ";commit;"))

    show_table_contents(engine, realplay_user_table)


def add_auth0_roles_column_to_dataframe(userid_email_tenant_df):
    logger.debug(" BEGIN  {}".format("add_auth0_roles_column_to_dataframe"))
    userid_email_tenant_df.rename(columns = {0 : 'user_id', 1 : 'email', 2 : 'tenant'}, inplace = True)

    userid_email_tenant_df['auth0_roles'] =  json.loads('""')

    show_dataframe(userid_email_tenant_df, 4)

    logger.info("\t\tdf columns are now : {} ".format(userid_email_tenant_df.columns))

    return userid_email_tenant_df


def database_driven_bulk_update_auth0_roles():
    logger.debug(" BEGIN  {}".format("database_driven_bulk_update_auth0_roles"))
    my_conn = db_connect_return_conn()

    # This section populates a dataframe from db
    #  adds 'auth0_roles' column to the dataframe
    #   updates a temp table
    #    updates realplay_user from the temp table

    userid_email_tenant_df = get_userid_email_tenant_from_db_sqlalchemy(my_conn)

    # show_dataframe(userid_email_tenant_df, 4)
    userid_email_tenant_roles_df = add_auth0_roles_column_to_dataframe(userid_email_tenant_df)
    show_dataframe(userid_email_tenant_roles_df)

    # this calls auth0 to get specific user data
    userid_email_tenant_roles_df = update_dataframe_from_auth0(my_conn, userid_email_tenant_roles_df)
    show_dataframe(userid_email_tenant_roles_df)

    bulk_load_temp_table(userid_email_tenant_roles_df)

    # This is an alternate path
    #  it loads the dataframe saved as a pickle file
    #   updates a temp table
    #    updates realplay_user from the temp table
    # update_table_from_pickle_file(my_conn, userid_email_tenant_df)

    return


if __name__ == '__main__':
    parser = configparser.ConfigParser()
    logger = logging.getLogger("RealplayExportProcess")

    # create the logs dir
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    create_app()
    logger.info('BEGIN process')
    overall_runtime_start = time()

    # test_log_messages()

    database_driven_bulk_update_auth0_roles()

    logger.info('END process')
