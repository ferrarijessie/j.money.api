from marshmallow import Schema, fields


class IncomeTypeSchema(Schema):
    name = fields.String(attribute="name")
    recurrent = fields.Boolean(attribute="recurrent")
    baseValue = fields.Float(attribute="base_value")

class IncomeReturnSchema(Schema):
    id = fields.Integer(attribute="id")
    typeId = fields.Integer(attribute="type_id")
    typeName = fields.String(attribute="type_name")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    received = fields.Boolean(attribute="received")

class IncomeTypeReturnSchema(Schema):
    incomeTypeId = fields.Integer(attribute="id")
    name = fields.String(attribute="name")
    recurrent = fields.Boolean(attribute="recurrent")
    baseValue = fields.Float(attribute="base_value")
    incomeValues = fields.List(fields.Nested(IncomeReturnSchema), required=False, attribute="income_values")

class IncomeInputSchema(Schema):
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    received = fields.Boolean(attribute="received")
    