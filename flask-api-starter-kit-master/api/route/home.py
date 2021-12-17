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

    print(result.get_auth0_async_mgmt_access_token())


    #thread_count = 4

    #for x in range(thread_count):
    #    #Path('thread-{}'.format(x)).touch()
    #    #asyncio.ensure_future(get_json_async(client, 'https://www.reddit.com/r/', ' thread-{} '.format(x)))
    #    asyncio.ensure_future(get_json_async(client, 'http://localhost/api/auth0_sync/', ' thread-{} '.format(x)))

    #asyncio.ensure_future(Auth0AsyncSchema(" thread-1"))
    #asyncio.ensure_future(Auth0AsyncSchema(" thread-2"))
    #asyncio.ensure_future(Auth0AsyncSchema(" thread-3"))

    #result="Launched {} threads".format(thread_count)

    print("home.py - result auth0_async" + str(result))
    return Auth0AsyncSchema().dump(result), 200


#async def get_json_async(client, url, my_thread):
#    async with client.get(url) as response:
#        Path(my_thread).touch()
#        print("\t\tGJS home.py - auth0_async - get_json - {} ".format(my_thread) )
#        assert response.status == 200
#        return await response.read()

