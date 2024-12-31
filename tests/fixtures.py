import pytest

from datetime import datetime

from database import db

from api.expenses.model import (
    Expense,
    ExpenseType,
    ExpenseCategoryEnum
)


# EXPENSES FACTORIES

class ExpenseTypeFactory(object):
    def create(self, **kwargs):
        data = {
            'id': ExpenseType.query.count() + 1,
            'name': 'Type 1',
            'category': ExpenseCategoryEnum.PERSONAL,
            'recurrent': False,
            'base_value': 0
        }
        data.update(kwargs)
        expense_type = ExpenseType(**data)
        db.session.add(expense_type)
        db.session.commit()
        return expense_type

@pytest.fixture(scope="function")
def expense_type_factory(request):
    return ExpenseTypeFactory()


class ExpenseFactory(object):
    def create(self, **kwargs):
        expense_type = ExpenseTypeFactory().create()

        data = {
            'id': Expense.query.count() + 1,
            'value': 100,
            'month': 1,
            'year': 2024,
            'type_id': expense_type.id,
            'paid': False
        }
        data.update(kwargs)
        expense = Expense(**data)
        db.session.add(expense)
        db.session.commit()
        return expense

@pytest.fixture(scope="function")
def expense_factory(request):
    return ExpenseFactory()
