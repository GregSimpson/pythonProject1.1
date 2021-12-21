from flask_marshmallow import Schema
from marshmallow.fields import Str


class ReportsSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["reports_process"]

    reports_process = Str()