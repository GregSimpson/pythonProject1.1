from flask_marshmallow import Schema
from marshmallow.fields import Str


class Auth0SyncSchema(Schema):
    class Meta:
        # Fields to expose
        #fields = ["message"]
        fields = ["auth0_sync"]

    #message = Str()
    auth0_sync = Str()