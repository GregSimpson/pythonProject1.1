from http import HTTPStatus
from ..model.auth0_sync import Auth0SyncModel
from ..model.auth0_async import Auth0AsyncModel
from ..model.async_example import AsyncExampleModel
from ..model.welcome import WelcomeModel
#from ..model.async_example import AsyncExampleModel

from ..schema.auth0_async import Auth0AsyncSchema
from ..schema.async_example import AsyncExampleSchema
from ..schema.auth0_sync import Auth0SyncSchema
from ..schema.async_example import AsyncExampleSchema
from ..schema.welcome import WelcomeSchema

from flasgger import swag_from
from flask import Blueprint

from ..src import auth0_controller as a0

import configparser

from pathlib import Path

# flask-api-starter-kit
# https://github.com/bajcmartinez/flask-api-starter-kit

# async threading example
# https://gist.github.com/vickumar1981/c3607805e2dd234c686eb6ca6c370ca2


import signal
import sys
import asyncio
import aiohttp
import json
import configparser
import logging

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)

home_api = Blueprint('api', __name__)
#logger = logging.getLogger("RealplaySync")


#-----
import os
import logging.config
import yaml
logger = logging.getLogger("RealplaySync")

def x_setup_logging(
    default_path='logging.yaml',
    default_level=logging.DEBUG,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

#-----





@home_api.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Welcome to the RealPlay Auth0 Role Sync',
            'schema': WelcomeSchema
        }
    }
})
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = WelcomeModel()
    #setup_logging()
    logger.debug(".")
    logger.debug("result welcome" + str(result))
    return WelcomeSchema().dump(result), 200



@home_api.route('/auth0_sync/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': '\t\tRealPlay Auth0 Role Sync - auth0_sync',
            'schema': Auth0SyncSchema
        }
    }
})
def auth0_sync():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = Auth0SyncModel()
    #setup_logging()
    logger.debug("/auth0_sync/ ")
    #print("home.py - result auth0_sync" + str(result))

    logger.debug ( result.get_auth0_sync_mgmt_access_token() )

    #print ( result.gjs1() )
    return Auth0SyncSchema().dump(result), 200


@home_api.route('/async_example/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': '\t\tRealPlay ASync Example - async_example',
            'schema': Auth0AsyncSchema
        }
    }
})
def async_example():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = AsyncExampleModel()
    #setup_logging()
    logger.debug("/async_example/ ")

    print(result.get_async_example_mgmt_access_token())
    print("home.py - result async_example" + str(result))
    return AsyncExampleSchema().dump(result), 200


@home_api.route('/auth0_async/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': '\t\tRealPlay Auth0 Role ASync - auth0_async',
            'schema': Auth0AsyncSchema
        }
    }
})
def auth0_async():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = Auth0AsyncModel()
    #setup_logging()
    logger.debug("/auth0_async/ ")
    print(result.get_auth0_async_mgmt_access_token())
    return Auth0AsyncSchema().dump(result), 200


@home_api.route('/logtest/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': '\t\tRealPlay logtest',
            'schema': Auth0AsyncSchema
        }
    }
})
def showloglevels():
    """
     Showloglevels 1 message from each log level
     ---
     """
    result = AsyncExampleModel()
    #setup_logging()
    logger.debug("/logtest/ ")
    print(result.showloglevels())


    print("home.py - result auth0_async" + str(result))
    return Auth0AsyncSchema().dump(result), 200


#async def get_json_async(client, url, my_thread):
#    async with client.get(url) as response:
#        Path(my_thread).touch()
#        print("\t\tGJS home.py - auth0_async - get_json - {} ".format(my_thread) )
#        assert response.status == 200
#        return await response.read()

@home_api.route('/workers/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': '\t\tRealPlay workers',
            'schema': a0.Auth0Controller
        }
    }
})
def workers():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = a0.Auth0Controller(logger)
    #setup_logging()
    logger.debug("/workers/ ")

    print(result.show_log_levels_auth0() )
    print("result.show_log_levels_auth0 " + str(result))
    print(result.yes_you_can_log_from_here())
    print("result.yes_you_can_log_from_here " + str(result))
    print(result.ok_now_we_can_build_things() )
    print("result.ok_now_we_can_build_things " + str(result))
    return AsyncExampleSchema().dump(result), 200

