from flask_marshmallow import Schema
from marshmallow.fields import Str


class AsyncExampleSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["async_example"]

    async_example = Str()