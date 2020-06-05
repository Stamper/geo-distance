from marshmallow import Schema, fields, ValidationError

class DistanceSchema(Schema):
    start = fields.Str(required=True)
    end = fields.Str(required=True)
    kilometers = fields.Decimal(required=True)
    miles = fields.Decimal(required=True)
