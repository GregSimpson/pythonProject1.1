#!/usr/bin/env python3

# https://www.practicepython.org/
'''
Take two lists, say for example these two:

  a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
  b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
and write a program that returns a list that contains only the elements that are common between
the lists (without duplicates). Make sure your program works on two lists of different sizes.

Extras:

Randomly generate two lists to test this
Write this in one line of Python (don’t worry if you can’t figure this out at this point - we’ll get to it soon)
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

if __name__ == "__main__":

    my_logger.info("\nscript START")

    maxRange = random.randint(15,20)
    rndsize1 = random.randint(8,maxRange)
    rndsize2 = random.randint(8,maxRange)

    my_logger.critical("crit msg  {0} ".format(66))
    my_logger.warning("warning msg  {0} ".format(87))
    my_logger.debug("maxRange == {0} ".format(maxRange))
    my_logger.error("rndsize1 == {0} ".format(rndsize1))
    my_logger.info("rndsize2 == {0} ".format(rndsize2))

    randomlist1 = random.sample(range(1, maxRange), rndsize1 - 1 )
    randomlist2 = random.sample(range(1, maxRange), rndsize2 - 1 )

    my_logger.debug("size {1} : \trandomlist1\t -- {0}".format(randomlist1,len(randomlist1) ) )
    my_logger.debug("size {1} : \trandomlist2\t -- {0}\n".format(randomlist2,len(randomlist2) ) )

    my_logger.debug("size {1} : \tintersection -- {0}".format(intersect(randomlist1,randomlist2),len(intersect(randomlist1,randomlist2))))
    my_logger.debug("size {1} : \tunion\t\t -- {0}".format(union(randomlist1, randomlist2),
                                                     len(union(randomlist1, randomlist2))))
    my_logger.debug("size {1} : \tdifference\t -- {0}".format(difference(randomlist1, randomlist2),
                                                     len(difference(randomlist1, randomlist2))))

    my_logger.info("\nscript END\n")

    i = 5
    count = 7
    print('-{:4d}:- {}'.format(i, (i * count)))
    print('-{:7d}:- {}'.format(i, (i * count)))

