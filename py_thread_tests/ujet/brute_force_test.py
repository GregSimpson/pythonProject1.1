

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



#import pandas as pd
# https://www.postgresql.org/docs/current/errcodes-appendix.html#ERRCODES-TABLE
#import psycopg2
import yaml
#from psycopg2 import extras
# sudo apt-get install python3.10-distutils
# python3.10 -m pip install opencv-python

from timeout import timeout, TimeoutError

from sqlalchemy import create_engine
from sqlalchemy import text
from config_db import config_db_from_env

def test_log_messages():
    logger.debug('test msg')
    logger.info('test msg')
    logger.warning('test msg')
    logger.error('test msg')
    logger.critical('test msg')

    #logger.debug('setting test : {}'.format(parser.get('ttec-realplay-parasol', 'client_domain')))


def create_app():
    setup_logging()
    load_settings_from_ini()

    return


def setup_logging():
    with open('./conf/logging.yaml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)
    logging.basicConfig(level=logging.DEBUG)
    #logger = logging.getLogger(__name__)


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


def call_ujet_manually():
    logger.debug(" in call_ujet_manually ")

    data = None

    # management API access token
    headers = {'content-type': "application/json"}
    #conn_str = parser.get(client_domain_param, 'client_domain')

    UserName = parser.get('UjetInfo', 'UserName')
    Password = parser.get('UjetInfo', 'Password')
    protocol = parser.get('UjetInfo', 'protocol')
    sub_domain = parser.get('UjetInfo', 'sub_domain')
    domain = parser.get('UjetInfo', 'domain')
    api_root = parser.get('UjetInfo', 'api_root')
    api_target = parser.get('UjetInfo', 'api_target')

    conn_str = ( parser.get('UjetInfo', 'sub_domain') + "." + parser.get('UjetInfo', 'sub_domain') )
    conn_api = (parser.get('UjetInfo', 'api_root') + "/" + parser.get('UjetInfo', 'api_target'))
    headers = ''

    logger.debug("\tUserName\t\t: {}".format(UserName))
    logger.debug("\tPassword\t\t: {}".format(Password))
    logger.debug("\tprotocol\t\t: {}".format(protocol))
    logger.debug("\tsub_domain\t\t: {}".format(sub_domain))
    logger.debug("\tdomain\t\t\t: {}".format(domain))
    logger.debug("\tapi_root\t\t: {}".format(api_root))
    logger.debug("\tapi_target\t\t: {}".format(api_target))
    logger.debug("\tconn_str\t\t: {}".format(conn_str))
    logger.debug("\tconn_api\t\t: {}".format(conn_api))



    payload = "{\"UserName\":\"" + \
              parser.get('UjetInfo', 'UserName') + \
              "\",\"Password\":\"" + \
              parser.get('UjetInfo', 'Password') + \
              "\"} " + protocol + "://" + \
              parser.get('UjetInfo', 'sub_domain') + \
              "." + parser.get('UjetInfo', 'domain') + \
              "/" + parser.get('UjetInfo', 'api_root') + \
              "/" + parser.get('UjetInfo', 'api_target')
    #logger.debug("\tpayload  : {}\n\n".format("payload details hidden"))
    logger.debug("\tpayload  : \n{}\n\n".format(payload))

    # TODO highlight
    ## NOTE - timeout simulator for debugging
    # random_sleep()

    try:
        logger.debug("Calling Ujet api\n")
        data_as_json = ""
        conn = http.client.HTTPSConnection(conn_str)


        conn.request("POST", conn_api, payload, headers)
        '''
        res = conn.getresponse()
        data = res.read()

        data_as_json = json.loads(data.decode('utf-8'))
        data_pretty_printed = json.dumps(data_as_json, indent=2, sort_keys=True)

        logger.debug(data_pretty_printed)
        '''
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

    #return data_as_json

if __name__ == '__main__':
    parser = configparser.ConfigParser()
    logger = logging.getLogger("brute_force_test")

    # create the logs dir
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    create_app()
    logger.info('BEGIN process')
    overall_runtime_start = time()

    #test_log_messages()

    call_ujet_manually()


