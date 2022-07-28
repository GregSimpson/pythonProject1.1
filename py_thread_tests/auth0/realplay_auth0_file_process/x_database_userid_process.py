##  install requirements from requirements.txt
# pip install -r requirements.txt

# TODO bulk insert options
# https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/

import configparser
import http
import http.client
import json
import logging.config
import os
import random
import subprocess
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from time import sleep, time

import pandas as pd
# https://www.postgresql.org/docs/current/errcodes-appendix.html#ERRCODES-TABLE
import psycopg2
import yaml

from config_db import config_db_from_ini
from timeout import timeout, TimeoutError


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


def load_settings():
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
    load_settings()

    return


def random_sleep(a=1, b=30):
    # prints a random value from the list
    list1 = [1, 2, 3, 4, 5]
    list2 = range(a, b)
    sleep_number = random.choice(list2)
    logger.debug("\t\tSleeping for {}".format(sleep_number))
    sleep(sleep_number)


# https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
@timeout(5)  # gjs
def call_auth0_to_get_certificate(client_domain_param, protocol="https"):
    logger.debug("client_domain_param: {} :: protocol: {}".format(client_domain_param, protocol))

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

    data = None
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

    # TODO create new exception type ?  maybe
    except Exception as error:
        if data is None:
            logging.error(" problem happened before data is initialized ")
        else:
            logging.error(data)
        return '{}'

    return data_as_json


# https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
@timeout(5)  # gjs
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

    # TODO - timeout simulator for debugging
    # random_sleep()

    conn.request("GET", conn_api, headers=headers)
    res = conn.getresponse()
    data = res.read()
    logger.debug(data)

    data_as_json = json.loads(data.decode('utf-8'))
    data_pretty_printed = json.dumps(data_as_json, indent=2, sort_keys=True)

    #  check result list for 'error'
    if 'error' in data_as_json:
        raise Auth0UserNotFoundException(data)

    logger.debug(data_pretty_printed)

    return data_pretty_printed


def log_this_summary_by_database(total_counter, total_todo, throttle_counter,
                                 throttle_sleep, number_of_sleeps, processed_to_be,
                                 processed_so_far, tenant_elapsed_time, timeout_counter, not_found_counter):
    tenant_elapsed_time = (time() - tenant_elapsed_time)
    overall_elapsed_time = (time() - overall_runtime_start)
    num_remaining_to_process = sum(processed_to_be.values()) - processed_so_far
    avg_time_per_userid = (overall_elapsed_time / processed_so_far)
    estimated_time_remaining = str(timedelta(seconds=(num_remaining_to_process * avg_time_per_userid)))

    # file process summary
    log_this_msg = '\n\n\tProcessed {} users total out of {} in this database' \
                   '\n\t\t\tsleeping every {} users for {} seconds {} times' \
                   '\n\t\t\t\tthis block time taken {}' \
                   '\n\t\toverall time taken : {}' \
                   '\n\t\t\taverage time per user : {}' \
                   '\n\n\tEstimated_time_remaining = {}  - not very reliable until late in the process' \
                   '\n\t\tprocess started at : {} (GMT) :: [MST = GMT - 7]' \
                   '\n\t\tprocess started at : {} (localtime)' \
                   '\n\n\tTimeouts encountered so far = {}' \
                   '\n\tNotFound encountered so far = {}' \
                   '\n\t\tsee the error log for details\n' \
        .format(total_counter,
                total_todo,
                throttle_counter,
                throttle_sleep,
                number_of_sleeps,
                str(timedelta(seconds=tenant_elapsed_time)),
                str(timedelta(seconds=overall_elapsed_time)),
                str(timedelta(seconds=avg_time_per_userid)),
                estimated_time_remaining,
                str(timedelta(seconds=overall_runtime_start)),
                format_time_stamp(overall_runtime_start, "%H:%M:%S"),
                timeout_counter, not_found_counter)
    logger.info(log_this_msg)


def log_this_summary_by_file(input_file_number, input_file_counter, full_path,
                             total_counter, file_line_count, throttle_counter,
                             throttle_sleep, number_of_sleeps, processed_to_be,
                             processed_so_far, tenant_elapsed_time, timeout_counter, not_found_counter):
    tenant_elapsed_time = (time() - tenant_elapsed_time)
    overall_elapsed_time = (time() - overall_runtime_start)
    num_remaining_to_process = sum(processed_to_be.values()) - processed_so_far
    avg_time_per_userid = (overall_elapsed_time / processed_so_far)
    estimated_time_remaining = str(timedelta(seconds=(num_remaining_to_process * avg_time_per_userid)))

    # file process summary
    log_this_msg = '\n\n\tProcessing {} files out of {} - {}' \
                   '\n\t\t{} users total out of {} for this tenant' \
                   '\n\t\t\tsleeping every {} users for {} seconds {} times' \
                   '\n\t\t\t\tthis block time taken {}' \
                   '\n\n\tProcessed {} users out of {} total from all tenants' \
                   '\n\t\toverall time taken : {}' \
                   '\n\t\t\taverage time per user : {}' \
                   '\n\n\tEstimated_time_remaining = {}  - not very reliable until late in the process' \
                   '\n\t\tprocess started at : {} (GMT) :: [MST = GMT - 7]' \
                   '\n\t\tprocess started at : {} (localtime)' \
                   '\n\n\tTimeouts encountered so far = {}' \
                   '\n\t\tsee the error log for details\n' \
        .format(input_file_number,
                input_file_counter,
                full_path,
                total_counter,
                file_line_count,
                throttle_counter,
                throttle_sleep,
                number_of_sleeps,
                str(timedelta(seconds=tenant_elapsed_time)),
                processed_so_far,
                sum(processed_to_be.values()),
                str(timedelta(seconds=overall_elapsed_time)),
                str(timedelta(seconds=avg_time_per_userid)),
                estimated_time_remaining,
                str(timedelta(seconds=overall_runtime_start)),
                format_time_stamp(overall_runtime_start, "%H:%M:%S"),
                timeout_counter,
                not_found_counter)
    logger.info(log_this_msg)


def format_time_stamp(result, format_str):
    # date = datetime.utcfromtimestamp(result)
    # output = datetime.strftime(date, "%H:%M:%S:%f")
    output = datetime.strftime(datetime.fromtimestamp(result), format_str)
    return output


def process_this_df_by_database(this_df, insert_writer, processed_to_be, processed_so_far, timeout_counter,
                                not_found_counter):
    tenant_elapsed_time = time()

    total_counter = 0
    user_counter = 0
    number_of_sleeps = 0
    throttle_counter = int(parser.get('Config_Data', 'throttle_counter', fallback="10"))
    throttle_sleep = int(parser.get('Config_Data', 'throttle_sleep', fallback="30"))
    # file_line_count = this_df.shape[0]

    for index, row in this_df.iterrows():
        try:
            # gjs - testing limit
            if user_counter >= throttle_counter:
                return processed_so_far, timeout_counter, not_found_counter

            # this pattern works for all except ttec-ped-developers domain
            tenant_domain = "ttec-realplay-" + row['tenant']

            # TODO highlight - Auth0 get_certificate
            auth0_certificate = call_auth0_to_get_certificate(tenant_domain)

            logger.info('client : {} - auth0_cert :: {}'.format(tenant_domain, auth0_certificate))
            if 'access_token' not in auth0_certificate:
                return

            # for index, row in this_df.iterrows():
            if user_counter >= throttle_counter:
                # TODO - just for debugging
                # exit(66)

                number_of_sleeps += 1
                # file process summary
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
                # TODO highlight - Auth0 get_role_data
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
            logging.info("domain {} - writing :{},{},{}".format(
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

            # TODO write to an array to update ???
            #  then add a bulk update :
            #  https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
            write_this_str = str(
                '\t\tinsert into realplay_auth0role_upload '
                '(userid, email, auth0_roles) values (\'{}\', \'{}\', \'{}\');'.format(
                    row['user_id'], email_str, json_str))

            logger.debug('\t{}\n'.format(write_this_str))
            insert_writer.write("{}\n".format(write_this_str))

        except Auth0UserNotFoundException as error:
            logger.error("\tAuth0UserNotFoundException  {}".format(" incrementing not_found_counter"))
            not_found_counter += 1
            log_psycopg2_exception_info(error, tenant_domain, row['user_id'], error.args)

        except TimeoutError as error:
            # TODO add this user to the (NEW) redo list
            logger.error("\tTimeoutError  {}".format(" incrementing timeout_counter"))
            timeout_counter += 1
            log_psycopg2_exception_info(error, tenant_domain, row['user_id'], error.args)

        except Exception as error:
            logger.error("\tUnKnown Exception  {}".format(error))
            log_psycopg2_exception_info(error, tenant_domain, row['user_id'], error.args)

    # file process summary
    log_this_summary_by_database(total_counter, len(this_df) - 1, throttle_counter, throttle_sleep,
                                 number_of_sleeps, processed_to_be, processed_so_far, tenant_elapsed_time,
                                 timeout_counter, not_found_counter)

    return processed_so_far, timeout_counter, not_found_counter


def log_psycopg2_exception_info(error, tenant_domain, user_id, args):
    logger.error("\tclient_domain_param : {}".format(tenant_domain))
    logger.error("\trow[\'user_id\']      : {}".format(user_id))
    logger.error("\terror.args            : {}".format(args))
    logger.error("\ttype(error)           : {}\n\n".format(type(error)))


# TODO - this might get the hook
def process_this_df_by_file(this_df, insert_writer, client_domain_param,
                            input_file_counter, input_file_number, full_path,
                            processed_to_be, processed_so_far, timeout_counter, not_found_counter):
    if client_domain_param != "ttec-realplay-postman-test":
        tenant_elapsed_time = time()
        # TODO highlight - Auth0 get_certificate
        auth0_certificate = call_auth0_to_get_certificate(client_domain_param)

        logger.info('client : {} - auth0_cert :: {}'.format(client_domain_param, auth0_certificate))
        if 'access_token' not in auth0_certificate:
            return

        total_counter = 0
        user_counter = 0
        number_of_sleeps = 0
        throttle_counter = int(parser.get('Config_Data', 'throttle_counter', fallback="10"))
        throttle_sleep = int(parser.get('Config_Data', 'throttle_sleep', fallback="30"))
        file_line_count = this_df.shape[0]

        for index, row in this_df.iterrows():
            if user_counter >= throttle_counter:
                number_of_sleeps += 1
                # file process summary
                log_this_summary_by_file(input_file_number, input_file_counter, full_path, total_counter,
                                         file_line_count, throttle_counter, throttle_sleep,
                                         number_of_sleeps, processed_to_be, processed_so_far, tenant_elapsed_time,
                                         timeout_counter, not_found_counter)

                sleep(throttle_sleep)
                user_counter = 0
                tenant_elapsed_time = time()
            total_counter += 1
            user_counter += 1
            processed_so_far += 1
            logger.debug('\n\n\tprocessed_so_far:{} - user_counter:{}'.format(processed_so_far, user_counter))

            try:
                parsed_roles = json.loads(
                    # TODO highlight - Auth0 get_role_data
                    call_auth0_to_get_role_data(auth0_certificate, client_domain_param, row['user_id']))
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
                logging.info("domain {} - writing :{},{},{}".format(
                    client_domain_param, row['user_id'], email_str, role_str))

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

                write_this_str = str(
                    '\t\tinsert into realplay_auth0role_upload '
                    '(userid, email, auth0_roles) values (\'{}\', \'{}\', \'{}\');'.format(
                        row['user_id'], email_str, json_str))

                logger.debug('\t{}\n'.format(write_this_str))
                insert_writer.write("{}\n".format(write_this_str))

            # TODO if this method is staying, clean up the exception handling
            # except TimeoutError as error:
            #    logger.error("\t\t\tTimeoutError  {}".format(error))
            except Exception as error:
                timeout_counter += 1
                # not_found_counter += 1
                logger.error("\tException  {}".format(error))
                logger.error("\tclient_domain_param : {}".format(client_domain_param))
                logger.error("\trow[\'user_id\']      : {}\n".format(row['user_id']))

        # file process summary
        log_this_summary_by_file(input_file_number, input_file_counter, full_path, total_counter,
                                 file_line_count, throttle_counter, throttle_sleep,
                                 number_of_sleeps, processed_to_be, processed_so_far, tenant_elapsed_time,
                                 timeout_counter,
                                 not_found_counter)

    return processed_so_far, timeout_counter, not_found_counter


def walk_level(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def add_suffix_sql(out1):
    '''
            update realplay_user
            set
                auth0_roles = realplay_auth0role_upload.auth0_roles
            from realplay_auth0role_upload
            where realplay_user.userid = realplay_auth0role_upload.userid
            and   realplay_user.auth0_roles::json::text != realplay_auth0role_upload.auth0_roles::json::text
            ;

        END
    $$;
    '''
    str_to_write = "\n\t\tupdate realplay_user\n\t\t\tset"
    out1.write(str_to_write)
    str_to_write = "\n\t\t\t\tauth0_roles = realplay_auth0role_upload.auth0_roles"
    out1.write(str_to_write)
    str_to_write = "\n\t\t\tfrom realplay_auth0role_upload"
    out1.write(str_to_write)
    str_to_write = "\n\t\t\twhere realplay_user.userid = realplay_auth0role_upload.userid"
    out1.write(str_to_write)
    str_to_write = "\n\t\t\t;"
    out1.write(str_to_write)

    str_to_write = "\n\tEND"
    out1.write(str_to_write)

    str_to_write = "\n$$;"
    out1.write(str_to_write)


def add_prefix_sql(out1):
    '''
    -- RealPlay realplay_auth0role_upload table
    DO $$
        BEGIN
            IF NOT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='realplay_auth0role_upload')
            THEN
                raise notice 'Creating  realplay_auth0role_upload table';
                create table realplay_auth0role_upload (
                  userid                    character varying(50)  NOT NULL,
                  email                     character varying(50)  NOT NULL,
                  auth0_roles               json
                );
            END IF;

            delete from realplay_auth0role_upload;
    '''
    # TODO clean this up
    str_to_write = "-- RealPlay realplay_auth0role_upload table\nDO $$\n\n\tBEGIN"
    out1.write(str_to_write)
    str_to_write = "\n\t\tIF NOT EXISTS(SELECT * FROM information_schema.tables" \
                   "WHERE table_name='realplay_auth0role_upload')\n\t\tTHEN"
    out1.write(str_to_write)

    str_to_write = "\n\t\t\traise notice 'Creating  realplay_auth0role_upload table';" \
                   "\n\t\t\tcreate table realplay_auth0role_upload ("
    out1.write(str_to_write)

    str_to_write = "\n\t\t\t\tuserid                    character varying(50)  NOT NULL,"
    out1.write(str_to_write)
    str_to_write = "\n\t\t\t\temail                     character varying(50)  NOT NULL,"
    out1.write(str_to_write)
    str_to_write = "\n\t\t\t\tauth0_roles               json"
    out1.write(str_to_write)
    str_to_write = "\n\t\t\t);\n\t\tEND IF;"
    out1.write(str_to_write)

    str_to_write = "\n\n\t\tDELETE FROM REALPLAY_AUTH0ROLE_UPLOAD;"
    out1.write(str_to_write)

    str_to_write = "\n\n"
    out1.write(str_to_write)


def renamer(file_to_rename):
    # change the file timestamp
    subprocess.check_output(['touch', ' ', file_to_rename])
    # rename the original file
    os.rename(file_to_rename, file_to_rename + '.processed')


def count_file_lines(file_path):
    return_number = 66  # set a default

    logger.debug('\n\tchecking {} '.format(file_path))
    #  if file exists
    if os.path.isfile(file_path):
        with open(file_path) as f:
            return_number = sum(1 for _ in f)

    logger.debug('\n\t\tCount for {} = {}'.format(file_path, return_number))

    return return_number


def backup_this_file(filename):
    #  if file exists - make a backup
    if os.path.isfile(filename):
        modified_time = os.path.getmtime(filename)
        timestamp = (datetime.fromtimestamp(modified_time).strftime("%b-%d-%y-%H:%M:%S"))
        backup_name = filename + timestamp
        # copy to the backup filename
        # subprocess.check_output(['cp ', insert_filename, backup_name])
        os.rename(filename, backup_name)


def open_output_file():
    logger.debug("opening output file - after backing up the existing output file")

    ## Getting the work directory (cwd)
    # source_dir = parser.get('user-export-file', 'source')

    output_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = parser.get('user-export-file', 'output_single_file')
    logger.info('\toutput_file    : {}'.format(output_file))

    insert_filename = ("{}/{}".format(output_dir, output_file))

    backup_this_file(insert_filename)

    new_output_file = open(insert_filename, 'w')
    add_prefix_sql(new_output_file)

    return new_output_file


def db_connect_return_conn():
    """ Return connection to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config_db_from_ini()

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
        # read connection parameters
        params = config_db_from_ini()

        # connect to the PostgreSQL server
        logger.debug('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("\tException  {}".format(error))

    return cur


def test_this_db_connection_by_cursor(cur):
    logger.debug('testing database connection')
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
        logger.debug(this_df.head())

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def get_userid_email_tenant_from_db_by_conn(my_conn):
    # https://towardsdatascience.com/how-to-convert-sql-query-results-to-a-pandas-dataframe-a50f0d920384
    dataframe = pd.read_sql(
        """SELECT USERID AS USER_ID, EMAIL, TENANT FROM REALPLAY_USER WHERE ACTIVE = 'true' ORDER BY 3,2""",
        my_conn)
    logger.info(dataframe.head())

    return dataframe


def get_userid_email_tenant_from_db_by_cursor(my_cursor):
    # https://stackabuse.com/working-with-postgresql-in-python/

    my_cursor.execute("SELECT USERID AS USER_ID, EMAIL, TENANT FROM REALPLAY_USER WHERE ACTIVE = 'true' ORDER BY 3,2")
    rows = my_cursor.fetchall()

    for row in rows:
        # logger.debug("\tUserid: " + row[0] + " \tEMAIL: " + row[1])
        logger.debug("\tUserid: " + row[0])


def generate_single_file_of_insert_stmts_from_database():
    out1 = open_output_file()
    source_dir = parser.get('user-export-file', 'source')

    # my_cursor = db_connect_return_cursor()
    # test_this_db_connection_by_cursor(my_cursor)
    # get_userid_email_tenant_from_db_by_cursor(my_cursor)

    my_conn = db_connect_return_conn()

    # test_this_db_connection_by_conn(my_conn)
    userid_email_df = get_userid_email_tenant_from_db_by_conn(my_conn)
    # logger.debug( (userid_email_df.head(50)) )

    logger.debug("open output file")

    processed_to_be = {}
    input_file_counter = 0
    processed_so_far = 0
    timeout_counter = 0
    not_found_counter = 0

    processed_so_far, timeout_counter, not_found_counter = process_this_df_by_database(userid_email_df, out1,
                                                                                       processed_to_be,
                                                                                       processed_so_far,
                                                                                       timeout_counter,
                                                                                       not_found_counter)
    add_suffix_sql(out1)

    return


def generate_single_file_of_insert_stmts_from_auth0_exports(json_or_csv="csv"):
    logger.debug("retrieve output file")
    out1 = open_output_file()
    source_dir = parser.get('user-export-file', 'source')

    if json_or_csv.startswith('.'):
        src_extension = "{}".format(json_or_csv)
    else:
        src_extension = ".{}".format(json_or_csv)

    processed_to_be = {}
    input_file_counter = 0
    processed_so_far = 0
    timeout_counter = 0
    not_found_counter = 0
    # r=root, d=directories, f = files
    for r, d, f in walk_level(source_dir, 0):
        for file in f:
            if file.endswith(src_extension):
                input_file_counter += 1
                processed_to_be[file] = count_file_lines('{}/{}'.format(source_dir, file)) - 1  # not counting headers

        log_this_msg = '\n\n\tDictionary processed_to_be - {}\n\t\tsum {} \n'.format(processed_to_be,
                                                                                     sum(processed_to_be.values()))
        logger.info(log_this_msg)

    input_file_number = 0
    # r=root, d=directories, f = files
    for r, d, f in walk_level(source_dir, 0):
        for file in f:
            if file.endswith(src_extension):
                full_path = os.path.join(r, file)
                file_root = os.path.splitext(file)[0]

                logger.info('\tNEW INPUT FILE     : {}\n\n'.format(full_path))
                logger.info('\tfull_path          : {}'.format(full_path))
                logger.info('\tsource_dir         : {}'.format(source_dir))
                logger.info('\tfile_root          : {}'.format(file_root))
                logger.info('\t# of input files   : {}'.format(input_file_counter))

                if src_extension == '.json':
                    this_df = pd.read_json(full_path, lines=True)
                if src_extension == '.csv':
                    this_df = pd.read_csv(full_path)

                logger.debug(this_df.style)
                input_file_number += 1

                # we now have a dataframe for this file
                #  loop over the rows - make a call to auth0/users to get the roles
                #  write the user_id,email, roles insert stms to a file

                processed_so_far, timeout_counter, not_found_counter = process_this_df_by_file(this_df, out1, file_root,
                                                                                               input_file_counter,
                                                                                               input_file_number,
                                                                                               full_path,
                                                                                               processed_to_be,
                                                                                               processed_so_far,
                                                                                               timeout_counter,
                                                                                               not_found_counter)

                #  move the processed file to ~~.processed
                renamer(full_path)

    add_suffix_sql(out1)


if __name__ == '__main__':
    parser = configparser.ConfigParser()
    logger = logging.getLogger("RealplayExportProcess")

    # tried to create logs dir dynamically - did not spend time to make it work
    # log_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    create_app()
    logger.info('BEGIN process')
    overall_runtime_start = time()

    # test_log_messages()

    # TODO fix the steps message
    # STEP 1 write one big file of insert statements
    logger.info("\n\n\nSTEP X")

    # realplay database driven
    generate_single_file_of_insert_stmts_from_database()

    # # can be either 'json' or 'csv'
    # generate_single_file_of_insert_stmts_from_auth0_exports(json_or_csv='csv')

    logger.info('END process')
