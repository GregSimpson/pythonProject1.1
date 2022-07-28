##  install requirements from requirements.txt
# pip install -r requirements.txt

# NOTE bulk insert options
# https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/

import configparser
import http
import http.client
import json
import logging.config
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

from config_db import config_db_from_ini
from config_db import config_db_from_env
from timeout import timeout, TimeoutErrorRealplay


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
                if k == 'tenant_list':
                    values_list = v.split(',')
                    #values_list = config['Config_Data']['tenant_list'].split(',')
                    #a = config.get(section,options).split(',')
                    for i in range(len(values_list)):
                        print("%s:::%s" % (k,  values_list[i]))
                logger.info(' {} = {}'.format(k, v))
            else:
                logger.info(' {} = {}'.format(k, 'hidden'))
        logger.info(' ')

    # TODO gjs
    # add env var reading for the DB connection info
    # also adjust settings.ini - remove the database definitions to avoid confusion


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

    logger.debug("\tconn_str : {}".format(conn_str))
    logger.debug("\tconn_api : {}".format(conn_api))
    logger.debug("\theaders  : {}".format(headers))
    logger.debug("\tpayload  : {}\n\n".format("payload details hidden"))

    ## timeout simulator for debugging
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

        # TODO create new exception type ?  maybe
        #  check result list for 'error'
        if 'error' in data_as_json:
            raise Exception(data)

        logger.debug("\n\n\t\tGood call to get certificate\n\n")

    # TODO handle new exception type ?  maybe
    except Exception as error:
        if data is None:
            logger.error(" problem happened before data is initialized ")
        else:
            logger.error(data)
        raise TimeoutErrorRealplay

    return data_as_json


# https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
@timeout(1)
def call_auth0_to_get_role_data(auth0_certificate, client_domain_param, user_name):
    logger.debug(
        "\tseeking tenant - {} :: userid - {}".format(parser.get(client_domain_param, 'client_domain'), user_name))

    headers = {'authorization': 'Bearer {}'.format(auth0_certificate['access_token'])}
    conn_str = parser.get(client_domain_param, 'client_domain')
    conn_api = "/api/v2/users/{}/roles".format(user_name)
    conn = http.client.HTTPSConnection(conn_str)

    logger.info("\tconn_str : {}".format(conn_str))
    logger.info("\tconn_api : {}".format(conn_api))
    logger.info("\theaders  : {}".format(headers))

    # NOTE - timeout simulator for debugging
    random_sleep(10)

    conn.request("GET", conn_api, headers=headers)
    res = conn.getresponse()
    data = res.read()
    # logger.debug(data)

    data_as_json = json.loads(data.decode('utf-8'))
    data_pretty_printed = json.dumps(data_as_json, indent=2, sort_keys=True)
    logger.info(data_pretty_printed)

    #  check result list for 'error'
    if 'error' in data_as_json:
        raise Auth0UserNotFoundException(data)

    return data_pretty_printed


def log_this_summary_by_database(total_counter, total_to_be_done, throttle_counter,
                                 throttle_sleep, number_of_sleeps, processed_to_be,
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
    log_this_msg = '\n\n\tProcessed {} users total out of {} in this database' \
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


def populate_auth0_role_column(this_df, processed_to_be, processed_so_far, timeout_counter, not_found_counter):
    tenant_elapsed_time = time()

    total_counter = 0
    user_counter = 0
    number_of_sleeps = 0
    throttle_counter = int(parser.get('Config_Data', 'throttle_counter', fallback="10"))
    throttle_sleep = int(parser.get('Config_Data', 'throttle_sleep', fallback="30"))

    for index, row in this_df.iterrows():
        try:
            # this pattern works for all except ttec-ped-developers domain
            tenant_domain = "ttec-realplay-" + row['tenant']

            # NOTE highlight - Auth0 get_certificate
            auth0_certificate = call_auth0_to_get_certificate(tenant_domain)

            logger.info('client : {} - auth0_cert :: {}'.format(tenant_domain, auth0_certificate))
            if 'access_token' not in auth0_certificate:
                return

            # for index, row in this_df.iterrows():
            if user_counter >= throttle_counter:
                # NOTE - just for debugging
                # if processed_so_far >= (10 * number_of_sleeps):
                # return processed_so_far, timeout_counter, not_found_counter
                # exit(66)
                # logger.debug("\n\n{}".format(this_df))

                # show_dataframe(this_df, 100)

                number_of_sleeps += 1
                # process summary
                log_this_summary_by_database(total_counter, len(this_df) - 1, throttle_counter, throttle_sleep,
                                             number_of_sleeps, processed_to_be, processed_so_far, tenant_elapsed_time,
                                             timeout_counter, not_found_counter)

                sleep(throttle_sleep)
                user_counter = 0
                tenant_elapsed_time = time()

            total_counter += 1
            user_counter += 1
            processed_so_far += 1
            logger.debug('\n\n\tprocessed_so_far:{} - user_counter:{}'.format(processed_so_far, user_counter))

            parsed_roles = json.loads(
                # NOTE highlight - Auth0 get_role_data
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
                                 number_of_sleeps, processed_to_be, processed_so_far, tenant_elapsed_time,
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
        # read connection parameters
        #params = config_db_from_ini()
        params = config_db_from_env()

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
    logger.debug('test_this_db_connection_by_conn BEGIN')
    try:
        this_df = pd.read_sql("""select version()""", conn)
        logger.debug("this_df :: {}".format(this_df.to_string()) )

        show_dataframe(this_df, 10)

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)

    logger.debug('test_this_db_connection_by_conn END')


def get_userid_email_tenant_from_db_by_conn(my_conn):
    # https://towardsdatascience.com/how-to-convert-sql-query-results-to-a-pandas-dataframe-a50f0d920384
    dataframe = pd.read_sql(
        """SELECT USERID AS USER_ID, EMAIL, TENANT FROM REALPLAY_USER WHERE ACTIVE = 'true' ORDER BY 3,2""",
        my_conn)
    pd.set_option('display.max_columns', None)

    # show_dataframe(dataframe,5)

    return dataframe


def get_userid_email_for_tenant_by_db_conn(my_conn, this_tenant):
    # https://towardsdatascience.com/how-to-convert-sql-query-results-to-a-pandas-dataframe-a50f0d920384

    # test_this_db_connection_by_conn(my_conn)

    sql_str = "SELECT USERID AS USER_ID, EMAIL, TENANT FROM REALPLAY_USER WHERE ACTIVE = 'true' and TENANT = \'{}\' ORDER BY 3,2".format(this_tenant)
    logger.debug("sql_str : {}".format(sql_str))
    dataframe = pd.read_sql(sql_str, my_conn)
    pd.set_option('display.max_columns', None)

    show_dataframe(dataframe, 5)

    return dataframe


def show_dataframe(df, limit=20):
    logger.debug(" show_dataframe BEGIN")
    role_counter = 1
    for index, row in df.iterrows():
        #if 'auth0_roles' in df:
        #    if (row['auth0_roles'] != '""') and (len(row['auth0_roles']) > 16):
        logger.debug("\n{} {}".format(role_counter, row))
        logger.debug(" - - - - - - - ")
        role_counter += 1
    logger.debug(" show_dataframe END")


def get_userid_email_tenant_from_db_by_cursor(my_cursor):
    # https://stackabuse.com/working-with-postgresql-in-python/

    my_cursor.execute("SELECT USERID AS USER_ID, EMAIL, TENANT FROM REALPLAY_USER WHERE ACTIVE = 'true' ORDER BY 3,2")
    rows = my_cursor.fetchall()

    # for row in rows:
    #    # logger.debug("\tUserid: " + row[0] + " \tEMAIL: " + row[1])


def update_dataframe_from_auth0(my_conn, userid_email_tenant_auth0_role_df):
    # userid_email_df = get_userid_email_tenant_from_db_by_conn(my_conn)
    # logger.debug( (userid_email_df.head(50)) )
    # show_dataframe(userid_email_tenant_auth0_role_df, 15)

    processed_to_be = {}
    input_file_counter = 0
    processed_so_far = 0
    timeout_counter = 0
    not_found_counter = 0

    processed_so_far, timeout_counter, not_found_counter = populate_auth0_role_column(userid_email_tenant_auth0_role_df,
                                                                                      processed_to_be,
                                                                                      processed_so_far,
                                                                                      timeout_counter,
                                                                                      not_found_counter)

    return userid_email_tenant_auth0_role_df


def show_table_contents(my_conn, temp_table_name='test_table'):
    logger.debug(" BEGIN  {} - {}".format("show_table_contents", temp_table_name))

    # https://towardsdatascience.com/how-to-convert-sql-query-results-to-a-pandas-dataframe-a50f0d920384
    sql_str = """SELECT * FROM {}""".format(temp_table_name)
    dataframe = pd.read_sql(
        sql_str,
        my_conn)
    show_dataframe(dataframe, 30)

    return dataframe


def bulk_load_temp_table(my_conn, df, page_size=100):
    logger.debug(" BEGIN  {}".format("bulk_load_temp_table"))
    table_name = 'test_table'
    """
    Using psycopg2.extras.bulk_load_temp_table() to insert the dataframe
    """
    # Create a list of tuples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s)" % (table_name, cols)

    logger.debug(cols)
    logger.debug(query)

    cursor = my_conn.cursor()
    try:
        make_a_temp_table(my_conn, table_name)
        extras.execute_batch(cursor, query, tuples, page_size)

        # show temp table contents
        #show_table_contents(my_conn, table_name)

        update_gjs_realplay_user_table(my_conn, table_name)
        #show_table_contents(my_conn, 'gjs_realplay_user')

        my_conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error: %s" % error)
        my_conn.rollback()
        cursor.close()
        return 1
    logger.debug("bulk_load_temp_table() done")
    # show_table_contents(my_conn, table_name)
    cursor.close()


def update_table_from_pickle_file(my_conn, df, page_size=100):
    logger.debug(" BEGIN  {}".format("update_table_from_pickle_file"))
    table_name = 'test_table'

    df = pd.read_pickle("saved_dataframe.pkl")
    # df = pd.read_pickle("gjs_dataframe.pkl")

    """
    Using psycopg2.extras.bulk_load_temp_table() to insert the dataframe
    """
    # Create a list of tuples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s)" % (table_name, cols)

    logger.debug(cols)
    logger.debug(query)

    cursor = my_conn.cursor()
    try:
        make_a_temp_table(my_conn, table_name)
        extras.execute_batch(cursor, query, tuples, page_size)

        # show temp table contents
        show_table_contents(my_conn, table_name)

        update_gjs_realplay_user_table(my_conn, table_name)
        show_table_contents(my_conn, 'gjs_realplay_user')

        my_conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error: %s" % error)
        my_conn.rollback()
        cursor.close()
        return 1
    logger.debug("bulk_load_temp_table() done")
    # show_table_contents(my_conn, table_name)
    cursor.close()


def add_auth0_roles_column(userid_email_tenant_df):
    logger.debug(" BEGIN  {}".format("add_auth0_roles_column"))

    userid_email_tenant_df['auth0_roles'] = '""'

    logger.debug("\t\tdf columns are now : {} ".format(userid_email_tenant_df.columns))
    # show_dataframe(userid_email_tenant_df, 4)

    return userid_email_tenant_df

def block_this_tenant(this_tenant):
    logger.debug(" BEGIN  {}".format("block_this_tenant({})".format(this_tenant)))
    my_conn = db_connect_return_conn()

    test_this_db_connection_by_conn(my_conn)

    block_these_df = get_userid_email_for_tenant_by_db_conn(my_conn, this_tenant)
    logger.debug(" new dataframe : \n{}".format(block_these_df.to_string()))

    # TODO
    # for each userid
    #    get auth0 cert
    #    api call to block user


def auth0_tenant_blocker():
    logger.debug(" BEGIN  {}".format("auth0_tenant_blocker"))

    # show the tenant_list - loop
    t_list = parser.get('Config_Data', 'tenant_list').split(',')
    #logger.debug("t-list type : {}".format(type(t_list)))
    #logger.debug("t-list      :\n\t{}".format(t_list))
    #logger.debug(x for x in t_list)

    [block_this_tenant(l) for l in t_list]



def database_driven_bulk_update_auth0_roles():
    logger.debug(" BEGIN  {}".format("database_driven_bulk_update_auth0_roles"))
    my_conn = db_connect_return_conn()

    # This section populates a dataframe from db
    #  adds 'auth0_roles' column to the dataframe
    #   updates a temp table
    #    updates realplay_user from the temp table
    userid_email_tenant_df = get_userid_email_tenant_from_db_by_conn(my_conn)
    # show_dataframe(userid_email_tenant_df, 4)
    userid_email_tenant_roles_df = add_auth0_roles_column(userid_email_tenant_df)
    userid_email_tenant_roles_df = update_dataframe_from_auth0(my_conn, userid_email_tenant_roles_df)
    bulk_load_temp_table(my_conn, userid_email_tenant_roles_df)

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

    auth0_tenant_blocker()

    logger.info('END process')
