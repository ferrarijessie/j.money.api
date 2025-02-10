from marshmallow import Schema, fields


class IncomeTypeSchema(Schema):
    name = fields.String(attribute="name")
    recurrent = fields.Boolean(attribute="recurrent")
    baseValue = fields.Float(attribute="base_value")

class IncomeReturnSchema(Schema):
    incomeId = fields.Integer(attribute="id")
    typeId = fields.Integer(attribute="type_id")
    incomeType = fields.String(attribute="income_type_name")
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

class IncomeCreateSchema(Schema):
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    received = fields.Boolean(attribute="received")

class IncomeUpdateSchema(Schema):
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    received = fields.Boolean(attribute="received")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    