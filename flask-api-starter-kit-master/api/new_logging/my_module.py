# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/

import new_logging

#logger = logging.getLogger(__name__)
logger = new_logging.getLogger(__name__)


def foo():
    logger.info('Hi, foo')

class Bar(object):
    def bar(self):
        logger.info('Hi, bar')

'''
import logging

# load my module
import my_module

# load the logging configuration
logging.config.fileConfig('logging.ini')

my_module.foo()
bar = my_module.Bar()
bar.bar()
'''

