from marshmallow import validate, fields, Schema, post_load
from app.models import Cabin

class CabinSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    level = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    capacity = fields.Int(required=True)
    data = fields.Nested('CabinDataSchema')

    @post_load
    def make_cabin(self, data, **kwargs):
        return Cabin(**data)