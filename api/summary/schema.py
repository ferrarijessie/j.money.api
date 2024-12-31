from marshmallow import Schema, fields


class SummaryReturnSchema(Schema):
    expensesTotal = fields.Float(attribute="expenses_total")
    incomesTotal = fields.Float(attribute="incomes_total")
    balance = fields.Float(attribute="balance")
