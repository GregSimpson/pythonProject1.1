from http import HTTPStatus

from ..model.auth0 import Auth0Model
from ..model.welcome import WelcomeModel
#from ..model.async_example import AsyncExampleModel

from ..schema.auth0 import Auth0Schema
from ..schema.async_example import AsyncExampleSchema
from ..schema.welcome import WelcomeSchema

from flasgger import swag_from
from flask import Blueprint

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



@home_api.route('/auth0_1/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': '\t\tRealPlay Auth0 Role Sync - auth0_1',
            'schema': Auth0Schema
        }
    }
})
def auth0_1x():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = Auth0Model()
    print("home.py - result auth0_1x" + str(result))

    print ( result.get_auth0_mgmt_access_token() )

    #print ( result.gjs1() )
    return Auth0Schema().dump(result), 200



