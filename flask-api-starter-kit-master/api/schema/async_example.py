from flask_marshmallow import Schema
from marshmallow.fields import Str


class AsyncExampleSchema(Schema):
    class Meta:
        # Fields to expose
        #fields = ["message"]
        fields = ["async1"]

    #message = Str()
    #auth0 = Str()
    async1 = Str()