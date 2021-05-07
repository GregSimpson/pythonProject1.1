#!/usr/bin/env python3

# https://www.practicepython.org/
'''
Ask the user for a string and print out whether this string is a palindrome or not.
(A palindrome is a string that reads the same forwards and backwards.)
'''

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

def intersect(a, b):
    """ return the intersection of two lists """
    my_logger.debug("\n\ta : {0}\n\tb : {1}".format(a, b))
    return list(set(a) & set(b))

def union(a, b):
    """ return the union of two lists """
    my_logger.debug("\n\ta : {0}\n\tb : {1}".format(a, b))
    return list(set(a) | set(b))


def is_palindrome(candidate):
    word_size = len(candidate)
    middle = round ( (word_size+1) / 2)
    my_logger.debug("\tcandidate {0} is {1} long".format(candidate, word_size))
    my_logger.debug("\tmiddle char is at {0} and is {1}".format(middle, candidate[middle - 1]))
    my_logger.debug("\tchar {0} is {1} ".format(0, candidate[0]))
    my_logger.debug("\tchar {0} is {1} ".format(word_size, candidate[word_size-1]))

    print(str(candidate) == str(candidate)[::-1])

    #mismatch = [w for w in word_list if w == w[::-1]]


    ## printing result
    #print ("Is the number palindrome ? : " + str(res))
    #mismatch =  [c for c in candidate if c == candidate[::-1]]
    #mismatch = [x for x in len(candidate) if (candidate[x] != candidate[ word_size - 1 - x]) ]
    mismatch = res = str(candidate) == str(candidate)[::-1]
    my_logger.debug("\tmismatch () ".format(mismatch) )

    for x in range(0, middle):
        my_logger.debug("\tforward  {} ".format(candidate[x]) )
        my_logger.debug("\t\tbackward {} ".format(candidate[ word_size - x - 1]))

    #print("x ::  {0} y :: {1} ".format( [ (candidate[x] , candidate[ word_size -1 -x]) for x in candidate if x < middle] ))

    #print("x ::  {} y :: {} ".format(    [(x,y) for x in candidate for y in candidate[::-1]] ) )
    #print("x ::  {} ".format( [(x) for x in candidate  if x <= middle] ))
    ##print("y ::  {} ".format( [(x) for x in candidate[::-1] ] ))
    #print("front ::  {}  back  :: {} ".format([(candidate[x], candidate[word_size - x - 1]) for x in range(0, word_size) ]))

    print("front ::  {}  back  :: {} ".format(x for x in range(0, word_size) ))

    #print("x ::  {} y :: {} ".format([(x, y) for x in candidate for y in candidate[::-1]]))
    pass


if __name__ == "__main__":

    my_logger.info("\nscript START")

    candidate = input("\n\nEnter a single word: ")
    my_logger.info("checking {0} to see if it is a palindrome. ".format(candidate))

    my_logger.info( is_palindrome(candidate) )

    my_logger.info("\nscript END\n")

