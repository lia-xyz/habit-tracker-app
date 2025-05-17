from marshmallow import Schema, fields

class LogSchema(Schema):
    date = fields.Date(required=True)