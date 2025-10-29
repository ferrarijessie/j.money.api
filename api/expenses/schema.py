from marshmallow import Schema, fields


class ExpenseTypeAcceptSchema(Schema):
    name = fields.String(attribute="name")
    category = fields.String(attribute="category")
    recurrent = fields.Boolean(attribute="recurrent")
    baseValue = fields.Float(attribute="base_value", required=False)
    endDate = fields.Date(attribute="end_date", required=False)


class ExpenseReturnSchema(Schema):
    id = fields.Integer(attribute="id")
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    paid = fields.Boolean(attribute="paid")
    typeName = fields.String(attribute="type_name")
    category = fields.String(attribute="category")


class ExpenseTypeReturnSchema(Schema):
    id = fields.Integer(attribute="id")
    name = fields.String(attribute="name")
    category = fields.String(attribute="get_category")
    recurrent = fields.Boolean(attribute="recurrent")
    baseValue = fields.Float(attribute="base_value")
    endDate = fields.Date(attribute="end_date")
    expenseValues = fields.List(fields.Nested(ExpenseReturnSchema), required=False, attribute="expense_values")


class ExpenseInputSchema(Schema):
    typeId = fields.Integer(attribute="type_id")
    value = fields.Float(attribute="value")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    paid = fields.Boolean(attribute="paid")
    