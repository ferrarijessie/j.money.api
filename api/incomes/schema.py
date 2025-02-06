from marshmallow import Schema, fields

class IncomeTypeReturnSchema(Schema):
    incomeTypeId = fields.Integer(attribute="id")
    name = fields.String(attribute="name")
    recurrent = fields.Boolean(attribute="recurrent")
    baseValue = fields.Float(attribute="base_value")

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

class IncomeCreateSchema(Schema):
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    received = fields.Boolean(attribute="received")

class IncomeUpdateSchema(Schema):
    value = fields.Float(attribute="value")
    received = fields.Boolean(attribute="received")
    