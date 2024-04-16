from marshmallow import validate, fields, Schema, post_load
from app.models import ReserveModels as Reserve

class ReserveSchema(Schema):
    id = fields.Int(dump_only=True)
    since = fields.Str(required=True)
    until = fields.Str(required=True)
    id_user = fields.Int(required=True)
    id_cabin = fields.Int(required=True)
    
    @post_load
    def make_reserve(self, data, **kwargs):
        return Reserve(**data)