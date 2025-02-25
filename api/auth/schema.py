from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(attribute="id")
    username = fields.String(attribute="username")
    password = fields.String(attribute="password")
    token = fields.String(attribute="token")

class UserUpdateSchema(Schema):
    username = fields.String(attribute="username")
