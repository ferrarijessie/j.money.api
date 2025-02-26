from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(attribute="id")
    username = fields.String(attribute="username")
    password = fields.String(attribute="password")
    token = fields.String(attribute="token")
    firstName = fields.String(attribute="first_name")
    lastName = fields.String(attribute="last_name")
    name = fields.String(attribute="name")
    email = fields.String(attribute="email")

class UserUpdateSchema(Schema):
    username = fields.String(attribute="username")
    firstName = fields.String(attribute="first_name")
    lastName = fields.String(attribute="last_name")
    email = fields.String(attribute="email")
