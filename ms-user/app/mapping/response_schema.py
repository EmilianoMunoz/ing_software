from marshmallow import validate, fields, Schema, post_load
from app.models import ResponseMessage

class ResponseSchema(Schema):
    message = fields.String(required=True, validate=validate.Length(min=1))
    status_code = fields.Integer(required=True)
    data = fields.Dict(required=False)

    @post_load
    def make_response(self, data, **kwargs):
        return ResponseMessage(**data)
