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

    logger.debug("type data {}\t {}\n".format(type(data), next(iter(data))))
    logger.debug("type data {}\t {}\n".format(type(data), data[next(iter(data))] ))
    logger.debug("type data {}\t {}\n".format(type(data), next(iter(  data[next(iter(data))] ))))

    logger.debug("\nGJS\n{} ::::".format(threadName))
    pretty( next(iter(  data[next(iter(data))] )) )
    logger.debug("\n::::\n\n")
    #ogger.debug("type data {}\t {}\n".format(type(data), next(iter(  data[next(iter(data))][0] ))))
    #logger.debug("type data[1] {}".format(type(data[])))


def process_data(threadName, q):
    #TODO add exception hamdling to exit thread
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            gjs_log_process_data(data, threadName)

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
    #dict test
    gjs_nameList =    { 'agents':
        [
            {'URL': 'url-data1', 'USERNAME': 'user1', 'PASSWORD': 'pass1', 'API_NAME': 'api-agents1', 'GOOGLE_QUEUE_NAME': 'google-q1'  }
        ]
    }
    logger.debug("gjs_test_dict_of_dicts :\n\t{}".format(gjs_nameList))



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

    # Fill the queue
    queueLock.acquire()
    for word in nameList:
        #workQueue.put(word)
        workQueue.put(gjs_nameList)
    queueLock.release()

    # Wait for queue to empty
    while not workQueue.empty():
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()

    logger.debug("shared_dict :\n{}".format(str(shared_dict)))
    #pretty(shared_dict)


    logger.debug("\nExiting Main Thread")
