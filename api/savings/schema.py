from marshmallow import Schema, fields


class SavingTypeSchema(Schema):
    name = fields.String(attribute="name")
    active = fields.Boolean(attribute="active")
    baseValue = fields.Float(attribute="base_value")    


class SavingValueReturnSchema(Schema):
    id = fields.Integer(attribute="id")
    typeId = fields.Integer(attribute="type_id")
    typeName = fields.String(attribute="type_name")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    used = fields.Boolean(attribute="used")


class SavingTypeReturnSchema(Schema):
    id = fields.Integer(attribute="id")
    name = fields.String(attribute="name")
    active = fields.Boolean(attribute="active")
    baseValue = fields.Float(attribute="base_value")
    savingValues = fields.List(fields.Nested(SavingValueReturnSchema), required=False, attribute="saving_values")


class SavingValueCreateSchema(Schema):
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    used = fields.Boolean(attribute="used")


class SavingValueUpdateSchema(Schema):
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    used = fields.Boolean(attribute="used")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")


class SavingsSummarySchema(Schema):
    typeId = fields.Integer(attribute="saving_type_id")
    name = fields.String(attribute="name")
    balance = fields.Float(attribute="balance")
    currentMonthValue = fields.Float(attribute="current_month_value")
