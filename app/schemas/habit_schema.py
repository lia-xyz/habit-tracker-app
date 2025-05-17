from marshmallow import Schema, fields, validate

class HabitSchema(Schema):
    title = fields.Str(required =True, validate=validate.Length(min=1, max=100))
    frequency = fields.Str(required=True, validate=validate.OneOf(['daily', 'weekly', 'monthly']))
    categories = fields.List(fields.Str(), load_default=[])