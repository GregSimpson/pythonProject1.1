
#  pip install -U pip setuptools wheel
#  pip install ruamel.yaml
import ruamel.yaml

import configparser
import logging.config
from pathlib import Path
from config_db import config_db_from_env

import yaml

from config_db import config_db_from_env
# read connection parameters
# params = config_db_from_ini()
params = config_db_from_env()

#LOGGER = singer.get_logger()

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


class BadDatabaseNameException(Error):
    """Raised when the specified database does not exist"""
    pass


def setup_log_dir():
    # create the logs dir
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)


def setup_logging():
    with open('./conf/logging.yaml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)


def load_settings_from_ini():
    yaml_file = open('conf/settings.ini', 'r')
    yaml_content = yaml.safe_load(yaml_file)

    logger.debug("Key: Value")
    for key, value in yaml_content.items():
        logger.debug(f"{type(key)} :: {type(value)}")
        logger.debug(f"{key}: {value}")
        #for k, v in parser.items(yaml_content):
        #    if k in ('client_id', 'client_secret', 'pswd', 'PASSWORD', 'Username'):
        #        logger.info(' {} = {}'.format(k, 'hidden'))

    return yaml_content


def test_log_messages():
    logger.debug('test msg')
    logger.info('test msg')
    logger.warning('test msg')
    logger.error('test msg')
    logger.critical('test msg')


def create_thread_array(num_of_threads):
    pass


def manage_threads(env_settings):
    logger.debug("\n\nmanage_threads BEGIN")

    #logger.debug("\n{}".format(env_settings))
    #for key, value in env_settings.items():
    #    logger.debug(f"{type(key)} :: {type(value)}")
    #   logger.debug(f"{key}: {value}")

    num_of_semaphores = env_settings['SYSTEM_ENV_VARS']['NUM_OF_SEMAPHORES']
    num_of_threads    = env_settings['SYSTEM_ENV_VARS']['NUM_OF_THREADS']
    random_sleep_range = env_settings['SYSTEM_ENV_VARS']['RANDOM_SLEEP_RANGE']

    logger.debug("\tNUM_OF_SEMAPHORES  : {}".format(num_of_semaphores))
    logger.debug("\tNUM_OF_THREADS     : {}".format(num_of_threads))
    logger.debug("\tRANDOM_SLEEP_RANGE : {}".format(random_sleep_range))

    thread_array = create_thread_array(num_of_threads)


def main():
    setup_log_dir()
    setup_logging()
    env_settings = load_settings_from_ini()

    manage_threads(env_settings)

    #test_log_messages()


if __name__ == '__main__':
    logger = logging.getLogger("allTogether")
    parser = configparser.ConfigParser()

    main()
