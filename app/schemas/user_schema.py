from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.Str(required =True, validate=validate.Length(min=3, max=30))
    email = fields.Email(required =True)
    password = fields.Str(required =True, load_only=True, validate=validate.Length(min=8))