from http import HTTPStatus
from ..model.auth0_sync import Auth0SyncModel
from ..model.welcome import WelcomeModel
#from ..model.async_example import AsyncExampleModel

from ..schema.auth0_sync import Auth0SyncSchema
from ..schema.async_example import AsyncExampleSchema
from ..schema.welcome import WelcomeSchema

from flasgger import swag_from
from flask import Blueprint

# flask-api-starter-kit
# https://github.com/bajcmartinez/flask-api-starter-kit

# async threading example
# https://gist.github.com/vickumar1981/c3607805e2dd234c686eb6ca6c370ca2


import signal
import sys
import asyncio
import aiohttp
import json

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)



home_api = Blueprint('api', __name__)


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
    print("home.py - result welcome" + str(result))
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
    print("home.py - result auth0_sync" + str(result))

    print ( result.get_auth0_sync_mgmt_access_token() )

    #print ( result.gjs1() )
    return Auth0SyncSchema().dump(result), 200



