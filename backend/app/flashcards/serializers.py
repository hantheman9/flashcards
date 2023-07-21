from marshmallow import fields
from app.utils.serializers import WrapDataSchema

class UserSchema(WrapDataSchema):
    #implement user schema
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password_hash = fields.String(required=True)

class FlashcardSchema(WrapDataSchema):
    id = fields.Int(dump_only=True)
    word = fields.Str(required=True)
    definition = fields.Str(required=True)
    bin = fields.Int()
    next_review_time = fields.DateTime()
    incorrect_count = fields.Int()
