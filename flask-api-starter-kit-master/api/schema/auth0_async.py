from flask_marshmallow import Schema
from marshmallow.fields import Str


class Auth0AsyncSchema(Schema):
    class Meta:
        # Fields to expose
        #fields = ["message"]
        fields = ["auth0_async"]

    #message = Str()
    auth0_async = Str()