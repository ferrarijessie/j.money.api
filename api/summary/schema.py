from marshmallow import Schema, fields


class SummaryReturnSchema(Schema):
    expensesTotal = fields.Float(attribute="expenses_total")
    incomesTotal = fields.Float(attribute="incomes_total")
    balance = fields.Float(attribute="balance")

class SummaryListReturnSchema(Schema):
    id = fields.Integer(attribute="id")
    value = fields.Float(attribute="value")
    typeName = fields.String(attribute="type_name")
    month = fields.Integer(attribute="month")
    year = fields.Integer(attribute="year")
    status = fields.Boolean(attribute="status")
    model = fields.String(attribute="model")
