from marshmallow import validate, fields, Schema, post_load
from app.models import User

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    surname = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(load_only=True)
    data = fields.Nested('UserDataSchema')

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)