from flask_marshmallow import Schema
from marshmallow.fields import Str


class Auth0Schema(Schema):
    class Meta:
        # Fields to expose
        #fields = ["message"]
        fields = ["auth0"]

    #message = Str()
    auth0 = Str()