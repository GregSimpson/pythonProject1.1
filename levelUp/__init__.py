#!/usr/bin/env python3

# https://levelup.gitconnected.com/22-code-snippets-that-every-python-programmer-must-learn-b7f7ec35e9df


import logging.handlers
import sys
from logging.handlers import RotatingFileHandler
import os
import random

FILENAME = os.path.basename(__file__)
#FILENAME = os.path.basename(__name__)
LOG_FILENAME = "./" + FILENAME + ".log"

# ## https://stackoverflow.com/questions/24505145/how-to-limit-log-file-size-in-python
my_logger = logging.getLogger()

#from logging.handlers import RotatingFileHandler
## 200 mb per log file, 5 files ~ approx 1GB
logging.basicConfig(
        handlers=[ RotatingFileHandler(LOG_FILENAME
                                      , mode='a'
                                      , maxBytes=200 * 1024 * 1024
                                      , backupCount=5
                                      , encoding=None
                                      ,delay=0)
               ],
        level=logging.DEBUG,
        format="%(levelname)-8s [%(asctime)s] :: %(funcName)s :: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S,%s"
)

# https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file
stdout_handler = logging.StreamHandler(sys.stdout)
my_logger.addHandler(stdout_handler)

def difference(a, b):
    """ return the difference between two lists """
    my_logger.debug("\n\ta : {0}\n\tb : {1}".format( a,b ))
    return (list(list(set(a) - set(b)) + list(set(b) - set(a))))

def mergeTwoDicts(d1, d2):
    return {**d1, **d2}

def chainComp(x):
    my_logger.debug(2 < x < 8)
    my_logger.debug(1 == x < 7)

def getLastElemInList(my_list):
    # Using brute force method
    last_element = my_list[len(my_list) - 1]
    my_logger.debug("\n\tbrute : {0}\n".format(last_element))

    # Using negative indexes
    last_element = my_list[-1]
    my_logger.debug("\n\tnegIndx : {0}\n".format(last_element))

    # Using pop method
    last_element = my_list.pop()
    my_logger.debug("\n\tpop-ed : {0}\n".format(last_element))


def get_vowels(string):
    return [vowel for vowel in string if vowel in 'aeiou']


def run_exec_time(t):
    total = 0
    for i in range(t):
        total += i
    my_logger.debug("\n\tcount : {0}".format(total) )


def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)
# End hms_string


def most_frequent(my_list2):
    return max(set(my_list2), key=my_list2.count)


if __name__ == "__main__":

    my_logger.info("\n\nscript START ============================\n")

    a, b = 2,4
    my_logger.debug("\n\ta : {0}\n\tb : {1}".format( a,b ))

    dict1 = dict(name="Joy", age="25")
    dict2 = {"name": "Joy", "city": "New York"}
    my_logger.info( mergeTwoDicts(dict1, dict2) )

    x = 5
    chainComp(x)

    my_list = ['banana', 'apple', 'orange', 'pineapple']
    getLastElemInList(my_list)

    someBigString = "Powder Donut. The big yellow dog chased the small black cat"
    my_logger.info( get_vowels(someBigString) )
    my_logger.info(set(get_vowels(someBigString)))


    # calc exec time
    import time
    start_time = time.time()
    run_exec_time(1000)
    end_time = time.time()
    time_taken = end_time - start_time
    my_logger.info("\t\tTime : {0}".format( time_taken ))
    my_logger.info("\t\tTime : {0}".format( hms_string(end_time - start_time) ) )


    # most freq
    mylist = [1, 1, 2, 3, 4, 5, 6, 6, 2, 2]
    my_logger.info("\n\t{0} is the most frequent item in\n\t\tis: {1}".format(most_frequent(mylist),  mylist))


# https://levelup.gitconnected.com/22-code-snippets-that-every-python-programmer-must-learn-b7f7ec35e9df
    # stopped after #8


    my_logger.info("\nscript END\n")

