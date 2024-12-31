from marshmallow import Schema, fields


class ExpenseTypeReturnSchema(Schema):
    expenseTypeId = fields.Integer(attribute="id")
    name = fields.String(attribute="name")
    category = fields.String(attribute="get_category")
    recurrent = fields.Boolean(attribute="recurrent")
    baseValue = fields.Float(attribute="base_value")


class ExpenseTypeAcceptSchema(Schema):
    name = fields.String(attribute="name")
    category = fields.String(attribute="category")
    recurrent = fields.Boolean(attribute="recurrent")
    baseValue = fields.Float(attribute="base_value")


class ExpenseReturnSchema(Schema):
    expenseId = fields.Integer(attribute="id")
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    paid = fields.Boolean(attribute="paid")


class ExpenseListReturnSchema(Schema):
    expenseId = fields.Integer(attribute="id")
    type = fields.String(attribute="type")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    paid = fields.Boolean(attribute="paid")
    category = fields.String(attribute="category")


class ExpenseCreateSchema(Schema):
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")


class ExpenseUpdateSchema(Schema):
    value = fields.Float(attribute="value")
    paid = fields.Boolean(attribute="paid")
    