##  install requirements from requirements.txt
# pip install -r requirements.txt

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
import yaml

from timeout import timeout


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

    conn = http.client.HTTPSConnection(conn_str)

    try:
        logger.debug("Calling auth0 to get certificate\n")

        conn.request("POST", conn_api, payload, headers)
        res = conn.getresponse()
        data = res.read()

        data_as_json = json.loads(data.decode('utf-8'))
        data_pretty_printed = json.dumps(data_as_json, indent=2, sort_keys=True)

        logger.debug(data_pretty_printed)
        conn.close()

        #  check result list for 'error'
        if 'error' in data_as_json:
            raise Exception(data)

        logger.debug("\n\n\t\tGood call to get certificate\n\n")

    except Exception as error:
        logging.error(data)
        return '{}'

    return data_as_json


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

    # TODO highlight
    #  NOTE - timeout simulator for debugging
    # random_sleep()

    conn.request("GET", conn_api, headers=headers)
    res = conn.getresponse()
    data = res.read()
    logger.debug(data)

    data_as_json = json.loads(data.decode('utf-8'))
    data_pretty_printed = json.dumps(data_as_json, indent=2, sort_keys=True)

    #  check result list for 'error'
    if 'error' in data_as_json:
        raise Exception(data)

    logger.debug(data_pretty_printed)

    return data_pretty_printed


def log_this_summary(input_file_number, input_file_counter, full_path,
                     total_counter, file_line_count, throttle_counter,
                     throttle_sleep, number_of_sleeps, processed_to_be,
                     processed_so_far, tenant_elapsed_time, timeout_counter):
    tenant_elapsed_time = (time() - tenant_elapsed_time)

    overall_elapsed_time = (time() - overall_runtime_start)
    log_this_msg = '\toverall_elapsed_time = {}'.format(overall_elapsed_time)
    logger.debug(log_this_msg)

    num_remaining_to_process = sum(processed_to_be.values()) - processed_so_far
    log_this_msg = '\tnum_remaining_to_process = {}'.format(num_remaining_to_process)
    logger.debug(log_this_msg)

    avg_time_per_userid = (overall_elapsed_time / processed_so_far)
    log_this_msg = '\tavg_time_per_userid = {}'.format(avg_time_per_userid)
    logger.debug(log_this_msg)

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
                format_result(overall_runtime_start, "%H:%M:%S"),
                timeout_counter)
    logger.info(log_this_msg)


def format_result(result, format_str):
    # date = datetime.utcfromtimestamp(result)
    # output = datetime.strftime(date, "%H:%M:%S:%f")

    output = datetime.strftime(datetime.fromtimestamp(result), format_str)
    return output


def process_this_df(this_df, insert_writer, client_domain_param,
                    input_file_counter, input_file_number, full_path,
                    processed_to_be, processed_so_far, timeout_counter):
    tenant_elapsed_time = time()

    # TODO highlight
    #  NOTE - Auth0 get_certificate
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
            log_this_summary(input_file_number, input_file_counter, full_path, total_counter,
                             file_line_count, throttle_counter, throttle_sleep,
                             number_of_sleeps, processed_to_be, processed_so_far, tenant_elapsed_time, timeout_counter)

            sleep(throttle_sleep)
            user_counter = 0
            tenant_elapsed_time = time()
        total_counter += 1
        user_counter += 1
        processed_so_far += 1
        logger.debug('\n\n\tprocessed_so_far:{} - user_counter:{}'.format(processed_so_far, user_counter))

        try:
            parsed_roles = json.loads(
                # TODO highlight
                #  NOTE - Auth0 get_role_data
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

        # except TimeoutError as error:
        #    logger.error("\t\t\tTimeoutError  {}".format(error))
        except Exception as error:
            timeout_counter += 1
            logger.error("\tException  {}".format(error))
            logger.error("\tclient_domain_param : {}".format(client_domain_param))
            logger.error("\trow[\'user_id\']      : {}\n".format(row['user_id']))

    # file process summary
    log_this_summary(input_file_number, input_file_counter, full_path, total_counter,
                     file_line_count, throttle_counter, throttle_sleep,
                     number_of_sleeps, processed_to_be, processed_so_far, tenant_elapsed_time, timeout_counter)

    return processed_so_far, timeout_counter


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
    str_to_write = "\n\t\t\t where realplay_user.userid = realplay_auth0role_upload.userid"
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
    str_to_write = "-- RealPlay realplay_auth0role_upload table\nDO $$\n\n\tBEGIN"
    out1.write(str_to_write)
    str_to_write = "\n\t\tIF NOT EXISTS(SELECT * FROM information_schema.tables" \
                   " WHERE table_name='realplay_auth0role_upload')\n\t\tTHEN"
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


def generate_single_file_of_insert_stmts_from_auth0_exports(json_or_csv="csv"):
    # Getting the work directory (cwd)
    source_dir = parser.get('user-export-file', 'source')

    output_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = parser.get('user-export-file', 'output_single_file')
    logger.info('\toutput_file    : {}'.format(output_file))

    insert_filename = ("{}/{}".format(output_dir, output_file))

    backup_this_file(insert_filename)

    out1 = open(insert_filename, 'w')
    add_prefix_sql(out1)

    if json_or_csv.startswith('.'):
        src_extension = "{}".format(json_or_csv)
    else:
        src_extension = ".{}".format(json_or_csv)

    processed_to_be = {}
    input_file_counter = 0
    processed_so_far = 0
    timeout_counter = 0
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

                processed_so_far, timeout_counter = process_this_df(this_df, out1, file_root,
                                                                    input_file_counter, input_file_number, full_path,
                                                                    processed_to_be, processed_so_far, timeout_counter)

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

    # STEP 1 write one big file of insert statements
    logger.info("\n\n\nSTEP 1 write one big file of insert statements")

    # ## can be either 'json' or 'csv'
    generate_single_file_of_insert_stmts_from_auth0_exports(json_or_csv='csv')

    logger.info('END process')
