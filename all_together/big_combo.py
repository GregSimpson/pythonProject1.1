# https://www.tutorialspoint.com/python/python_multithreading.htm

#!/usr/bin/python

import json
import logging.config
from multiprocessing import Process, Manager
from pathlib import Path
import queue
import threading
import time
import yaml
# sudo apt-get install python-yaml
# pip install pyyaml
# sudo apt-get install python3-ruamel.yaml
import ruamel.yaml
from config_db import config_db_from_env

#-----------------

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
import time
from time import sleep



#import pandas as pd
# https://www.postgresql.org/docs/current/errcodes-appendix.html#ERRCODES-TABLE
#import psycopg2
import yaml
#from psycopg2 import extras
# sudo apt-get install python3.10-distutils
# python3.10 -m pip install opencv-python

from timeout import timeout, TimeoutError

#from sqlalchemy import create_engine
#from sqlalchemy import text
from config_db import config_db_from_env

#--------------

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print("Starting " + self.name)
        process_data(self.name, self.q)
        print("Exiting " + self.name)


def load_settings_from_ini():
    print("IN load_settings_from_ini ")
    yaml_file = open('conf/settings.ini', 'r')
    #yaml_file = open('dict_def.yaml', 'r')
    yaml_content = yaml.safe_load(yaml_file)

    logger.debug("Key: Value")
    for key, value in yaml_content.items():
        print("loading {} : {}\n".format(key,value))

        logger.debug(f"{type(key)} :: {type(value)}")
        logger.debug(f"{key}: {value}")
        #for k, v in parser.items(yaml_content):
        #    if k in ('client_id', 'client_secret', 'pswd', 'PASSWORD', 'Username'):
        #        logger.info(' {} = {}'.format(k, 'hidden'))

    return yaml_content

def test_log_messages():
    logger.debug('\ttest msg')
    logger.info(' \ttest msg')
    logger.warning('\ttest msg')
    logger.error('\ttest msg')
    logger.critical('\ttest msg')


def gjs_log_process_data(data, threadName):
    #print("%s processing %s\n" % (threadName, data))
    logger.debug("{} processing   {}\n".format(threadName, data))

    logger.debug("type data {}\t\n\t{}\n".format(type(data), next(iter(data))))
    logger.debug("type data {}\t\n\t{}\n".format(type(data), data[next(iter(data))] ))
    logger.debug("type data {}\t\n\t{}\n".format(type(data), next(iter(  data[next(iter(data))] ))))

    logger.debug("\nGJS {} ::::".format(threadName))
    pretty( next(iter(  data[next(iter(data))] )) )
    logger.debug("\n")
    #ogger.debug("type data {}\t {}\n".format(type(data), next(iter(  data[next(iter(data))][0] ))))
    #logger.debug("type data[1] {}".format(type(data[])))


def process_data(threadName, q):
    #TODO add exception hamdling to exit thread
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            ##gjs_log_process_data(data, threadName)
            #logger.debug("threadName:{} - I would call this url".format(threadName))
            #logger.debug("{}".format(data))
            ##pretty(data)

            #shared_str = "threadName:{}\nI would append the results of {} to 'shared-dict'\n\n".format(threadName,data['final_url'])

            shared_str = "threadName:{}\nI would call google with the results of\n{}\n{}\n\n".format(threadName,data['final_url'],data['params'])
            #logger.debug(shared_str)
            shared_dict[data['final_url']] = shared_str

            # AFTER the ujet api call - save the results - for debugging
            #shared_dict[data] = threadName
            #shared_dict[data[1]] = data

        else:
            queueLock.release()
        time.sleep(1)


def setup_log_dir():
    # create the logs dir
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)


def setup_logging():
    with open('./conf/logging.yaml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)


def pretty(d, indent=0):
    for key, value in d.items():
        #logger.debug('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            logger.debug("{} - {} ".format(str(key), '\t' * (indent+1) + str(value)))
            #logger.debug('\t' * (indent+1) + str(value))
            pass


# TODO define main - done
# TODO add logging - done
# TODO read from yaml - done
# TODO shared dict - done
# use env for number threads - done
# pass info to the thread when you build it - done

## !!!! GJS left to do "
# TODO generate the dicts to pass to each thread
# TODO make the api calls
# TODO load shared-dict from api results

# TODO connect to GOOGLE queues
# TODO post to GOOGLE queues


def generate_thread_list(env_settings):
    num_threads = env_settings['SYSTEM_ENV_VARS']['NUM_OF_THREADS']
    logger.debug("Creating {} new threads".format(num_threads))
    return_me = []

    for t in range(1,num_threads+1):
        return_me.append("Gjs-Thread-{}".format(t))

    logger.debug("\n\nNEW threadlist says\n\n {}".format(return_me))
    return return_me


def generate_api_info_from_settings(env_settings):
    logger.debug("running {}".format(generate_api_info_from_settings))

    return_me = []

    #logger.debug("type of env_settings: {}\n\n".format(type(env_settings)))
    google_dict, ujet_dict = handle_complex_thing(env_settings)

    #pretty(ujet_dict)

    ## -- loop over these
    ## from API_TARGET_DICTS
    ujet_api_target_dicts = env_settings['UJET_ENV_VARS']['UjetManagerApiGets']['API_TARGET_DICTS']
    # loop over this dict
    #logger.debug( "\n\n LOOPING ujet_api_target_dicts \n".format())

    for dict_key, dict_value in ujet_api_target_dicts.items():
        gjs_dict = {}
        #logger.debug("Api Group : {}".format(dict_key))
        ujet_api_name = env_settings['UJET_ENV_VARS']['UjetManagerApiGets']['API_TARGET_DICTS'][dict_key]['API_NAME']
        #ujet_dict['final_url'] = ujet_dict['ujet_url'] + '/' + ujet_api_name
        gjs_dict['final_url'] = ujet_dict['ujet_url'] + '/' + ujet_api_name
        gjs_dict['params'] = ujet_dict
        return_me.append(gjs_dict)

        #ujet_google_queue_name = env_settings['UJET_ENV_VARS']['UjetManagerApiGets']['API_TARGET_DICTS'][dict_key]['GOOGLE_QUEUE_NAME']

        #logger.debug("ujet_api_name          : {}".format(ujet_api_name))
        #logger.debug("ujet_dict['final_url']          : {}".format(ujet_dict['final_url']))
        #####return_me.append(ujet_dict)
        #logger.debug("ujet_dict          : {}".format(ujet_dict))
        #logger.debug("\n\nreturn_me          : \n{}\n".format(return_me))

    return return_me


    #    logger.debug("ujet_google_queue_name : {}\n\n".format(ujet_google_queue_name))


    #ujet_dict['ujet_url'] = UJET_API_URL_STR
    #ujet_dict['ujet_header'] = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']
    #ujet_dict['USERNAME'] = env_settings['UJET_ENV_VARS']['UjetCreds']['USERNAME']
    #ujet_dict['PASSWORD'] = env_settings['UJET_ENV_VARS']['UjetCreds']['PASSWORD']


    #gjs_nameList =    { 'agents':
    #    [
    #        {'URL': 'url-data1', 'USERNAME': 'user1', 'PASSWORD': 'pass1', 'API_NAME': 'api-agents1', 'GOOGLE_QUEUE_NAME': 'google-q1'  }
    #    ]
    #}
    #logger.debug("gjs_test_dict_of_dicts :\n\t{}".format(gjs_nameList))
    #for dict_key, dict_item in env_settings.items():
    #    logger.debug("dict_key: {}\tdict_item: \t{} \n\t{}".format(dict_key,type(dict_item), dict_item))
    #    #for tuple_item in dict_item:
    #    #    logger.debug("tuple parts: \t{}\n\t{}\n\n".format(type(tuple_item), tuple_item))
    #for key in env_settings:
    #    logger.debug("key: {}".format(key))

    #exit(66)



def handle_complex_thing( handle_this , tabs=1):

    #system_dict = {}
    google_dict = {}
    ujet_dict = {}

    logger.debug("in handle_complex_thing: type is : {} ".format(type(handle_this)))


    #system_dict['RANDOM_SLEEP_RANGE'] = env_settings['SYSTEM_ENV_VARS']['RANDOM_SLEEP_RANGE']

    google_dict['USERNAME'] = env_settings['GOOGLE_ENV_VARS']['GoogleCreds']['USERNAME']
    google_dict['PASSWORD'] = env_settings['GOOGLE_ENV_VARS']['GoogleCreds']['PASSWORD']

    google_dict['PROTOCOL'] = env_settings['GOOGLE_ENV_VARS']['GoogleBaseURL']['PROTOCOL']
    google_dict['SUB_DOMAIN'] = env_settings['GOOGLE_ENV_VARS']['GoogleBaseURL']['SUB_DOMAIN']
    google_dict['DOMAIN'] = env_settings['GOOGLE_ENV_VARS']['GoogleBaseURL']['DOMAIN']


    #ujet_dict['USERNAME'] = env_settings['UJET_ENV_VARS']['UjetCreds']['USERNAME']
    #ujet_dict['PASSWORD'] = env_settings['UJET_ENV_VARS']['UjetCreds']['PASSWORD']

    #ujet_dict['PROTOCOL'] = env_settings['UJET_ENV_VARS']['UjetBaseURL']['PROTOCOL']
    #ujet_dict['SUB_DOMAIN'] = env_settings['UJET_ENV_VARS']['UjetBaseURL']['SUB_DOMAIN']
    #ujet_dict['DOMAIN'] = env_settings['UJET_ENV_VARS']['UjetBaseURL']['DOMAIN']

    #ujet_dict['Accept'] = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']['Accept']
    #ujet_dict['User-Agent'] = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']['User-Agent']
    #ujet_dict['Content-Length'] = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']['Content-Length']
    #ujet_dict['Connection'] = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']['Connection']
    #ujet_dict['Accept-Encoding'] = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']['Accept-Encoding']


    #ujet_dict['METHOD'] = env_settings['UJET_ENV_VARS']['UjetManagerApiGets']['METHOD']
    #ujet_dict['API_ROOT'] = env_settings['UJET_ENV_VARS']['UjetManagerApiGets']['API_ROOT']

    #pretty(google_dict)
    #pretty(ujet_dict)

    UJET_API_URL_STR = env_settings['UJET_ENV_VARS']['UjetBaseURL']['PROTOCOL'] + '://'
    UJET_API_URL_STR = UJET_API_URL_STR + '/' + env_settings['UJET_ENV_VARS']['UjetBaseURL']['SUB_DOMAIN']
    UJET_API_URL_STR = UJET_API_URL_STR + '/' + env_settings['UJET_ENV_VARS']['UjetBaseURL']['DOMAIN']
    UJET_API_URL_STR = UJET_API_URL_STR + '/' + env_settings['UJET_ENV_VARS']['UjetManagerApiGets']['API_ROOT']

    #logger.debug("\n UJET_API_URL_STR\t: {}".format(UJET_API_URL_STR))
    #logger.debug("\n UJET_HEADER_STR\t: {}".format(env_settings['UJET_ENV_VARS']['UjetApiHEADERS']))
    #ogger.debug("\n UjetCreds\t\t: {}".format(env_settings['UJET_ENV_VARS']['UjetCreds']))

    ujet_dict['ujet_url'] = UJET_API_URL_STR
    ujet_dict['ujet_header'] = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']
    ujet_dict['USERNAME'] = env_settings['UJET_ENV_VARS']['UjetCreds']['USERNAME']
    ujet_dict['PASSWORD'] = env_settings['UJET_ENV_VARS']['UjetCreds']['PASSWORD']


    # -------------------
    ##APPS APIs
    #UJET_BASE = "https://ttecphoenix-5x4khsz.uc1.ccaiplatform.com/apps/api/v1/"
    #UJET_API = "wait_times?lang=en"

    #URL = UJET_BASE + UJET_API



    #logger.debug("UJET_HEADER_STR\t: {}".format(UJET_HEADER_STR))

    HEADERS = { \
        'Content-Length': '0', \
        'User-Agent': "tap-ujet greg.simpson@ttec.com", \
        'Accept': '*/*', \
        'Accept-Encoding': 'gzip, deflate, br', \
        'Connection': 'keep-alive' \
        }

    #print(URL)
    #print(USERNAME)
    #print(PASSWORD)
    #print(HEADERS)

    #g = requests.get(
    #    url=URL,
    #    auth=(USERNAME, PASSWORD),
    #    json=None,
    #    headers=HEADERS)
    #print(g.json())


    ## from SYSTEM_ENV_VARS
    ##random_sleep_range = env_settings['SYSTEM_ENV_VARS']['RANDOM_SLEEP_RANGE']


    ##logger.debug( "random_sleep_range: {}".format(random_sleep_range))


    # from GOOGLE_ENV_VARS
    #google_user = env_settings['GOOGLE_ENV_VARS']['GoogleCreds']['USERNAME']
    #google_pswd = env_settings['GOOGLE_ENV_VARS']['GoogleCreds']['PASSWORD']

    #logger.debug( "google_user       : {}".format(google_user))
    #logger.debug( "google_pswd       : {}".format(google_pswd))

    #
    #google_protocol = env_settings['GOOGLE_ENV_VARS']['GoogleBaseURL']['PROTOCOL']
    #google_sub_domain = env_settings['GOOGLE_ENV_VARS']['GoogleBaseURL']['SUB_DOMAIN']
    #oogle_domain = env_settings['GOOGLE_ENV_VARS']['GoogleBaseURL']['DOMAIN']

    #logger.debug( "google_protocol   : {}".format(google_protocol))
    #logger.debug( "google_sub_domain : {}".format(google_sub_domain))
    #logger.debug( "google_domain     : {}\n".format(google_domain))



    # from UJET_ENV_VARS
    #ujet_user = env_settings['UJET_ENV_VARS']['UjetCreds']['USERNAME']
    #ujet_pswd = env_settings['UJET_ENV_VARS']['UjetCreds']['PASSWORD']

    #logger.debug( "ujet_user         : {}".format(ujet_user))
    #logger.debug( "ujet_pswd         : {}".format(ujet_pswd))


    # from UjetBaseURL
    #ujet_protocol = env_settings['UJET_ENV_VARS']['UjetBaseURL']['PROTOCOL']
    #ujet_sub_domain = env_settings['UJET_ENV_VARS']['UjetBaseURL']['SUB_DOMAIN']
    #ujet_domain = env_settings['UJET_ENV_VARS']['UjetBaseURL']['DOMAIN']


    #logger.debug( "ujet_protocol     : {}".format(ujet_protocol))
    #logger.debug( "ujet_sub_domain   : {}".format(ujet_sub_domain))
    #logger.debug( "ujet_domain       : {}".format(ujet_domain))

    # from UjetApiHEADERS
    #ujet_hdr_accept = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']['ACCEPT']
    #ujet_hdr_user_agent = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']['USER-AGENT']
    #ujet_hdr_content_type = env_settings['UJET_ENV_VARS']['UjetApiHEADERS']['CONTENT-TYPE']


    #logger.debug( "ujet_hdr_accept       : {}".format(ujet_hdr_accept))
    #logger.debug( "ujet_hdr_user_agent   : {}".format(ujet_hdr_user_agent))
    #logger.debug( "ujet_hdr_content_type : {}".format(ujet_hdr_content_type))

    # from UjetManagerApiGets
    #ujet_api_get_method = env_settings['UJET_ENV_VARS']['UjetManagerApiGets']['METHOD']
    #ujet_api_root = env_settings['UJET_ENV_VARS']['UjetManagerApiGets']['API_ROOT']


    #logger.debug( "ujet_api_get_method : {}".format(ujet_api_get_method))
    #logger.debug( "ujet_api_root       : {}".format(ujet_api_root))


    return google_dict, ujet_dict





    '''
    if type(handle_this) is dict:
        for dict_key, dict_item in handle_this.items():
            logger.debug("\ndict_key: {}".format(dict_key))
            if dict_item is not None:
                logger.debug("\ndict_item: {} : tabs = {} \n{}{}".format(type(dict_item), tabs, '\t'*tabs, dict_item))
                handle_complex_thing(dict_item, tabs+1)
    '''


if __name__ == '__main__':

    logger = logging.getLogger("allTogether")
    setup_log_dir()
    setup_logging()
    env_settings = load_settings_from_ini()

    logger.debug("\nStarting Main Thread")

    logger.debug("the yaml file says:\n\t")
    pretty (env_settings)

    #test_log_messages()

    manager = Manager()
    shared_dict = manager.dict()


    # number is defined by NUM_OF_THREADS in yaml
    threadList = generate_thread_list(env_settings)
    #threadList = ["Thread-1", "Thread-2", "Thread-3"]

    # names here are defined by the QUEUE_NAMES in yaml (yet to be defined)
    #  each API writes to a queue - some apis use the same queue
    nameList = ["One", "Two", "Three", "Four", "Five", "six", "seven"]
    #TODO - generate this from yaml info
    #  it will look something like this (I think)
    gjs_generated_name_list = generate_api_info_from_settings(env_settings)

    #logger.debug("gjs_generated_name_list :\n{}".format(gjs_generated_name_list))
    #exit(66)

    ###dict test
    #gjs_nameList =    { 'agents':
    #    [
    #        {'URL': 'url-data1', 'USERNAME': 'user1', 'PASSWORD': 'pass1', 'API_NAME': 'api-agents1', 'GOOGLE_QUEUE_NAME': 'google-q1'  }
    #    ]
    #}
    #logger.debug("gjs_test_dict_of_dicts :\n\t{}".format(gjs_nameList))



    queueLock = threading.Lock()
    # workQueue = Queue.queue(10) # works - bigger than list size
    #workQueue = queue.Queue(6)  # fails - smaller than list size
    ##workQueue = queue.Queue(len(nameList))
    workQueue = queue.Queue()
    threads = []
    threadID = 1

    # Create new threads
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # ORIG
    ## Fill the queue
    #queueLock.acquire()
    #for word in nameList:
    #    workQueue.put(word)
    #queueLock.release()

    #for word in gjs_generated_name_list:
    #    logger.debug("gjs_generated_name_list : \n{}".format(word))
    #exit(66)

    # MY Fill the queue
    queueLock.acquire()
    for word in gjs_generated_name_list:
        workQueue.put(word)
    queueLock.release()

    # Wait for queue to empty
    while not workQueue.empty():
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()

    #logger.debug("shared_dict :\n{}".format(str(shared_dict)))
    pretty(shared_dict)


    logger.debug("\nExiting Main Thread")
