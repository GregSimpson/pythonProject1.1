import logging

logger = logging.getLogger(__name__)
logger.warn('warning log message')

def foo():
    logger.debug('depending on configuration this may not be printed')
    logger.info('Log message from function foo.')