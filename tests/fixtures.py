import pytest

from datetime import datetime

from database import db

from api.expenses.model import (
    Expense,
    ExpenseType,
    ExpenseCategoryEnum
)
from api.incomes.model import (
    Income,
    IncomeType
)
from api.savings.model import (
    SavingType,
    SavingValue
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


#  INCOMES FIXTURES

class IncomeTypeFactory(object):
    def create(self, **kwargs):
        data = {
            'id': IncomeType.query.count() + 1,
            'name': 'Income 1',
            'base_value': 1000,
        }
        data.update(kwargs)
        income_type = IncomeType(**data)
        db.session.add(income_type)
        db.session.commit()
        return income_type

@pytest.fixture(scope="function")
def income_type_factory(request):
    return IncomeTypeFactory()


class IncomeFactory(object):
    def create(self, **kwargs):
        income_type = IncomeTypeFactory().create()
        data = {
            'id': Income.query.count() + 1,
            'value': 100,
            'month': 9,
            'year': 2024,
            'type_id': income_type.id,
            'received': False
        }
        data.update(kwargs)
        income = Income(**data)
        db.session.add(income)
        db.session.commit()
        return income

@pytest.fixture(scope="function")
def income_factory(request):
    return IncomeFactory()


#  SAVINGS FIXTURES

class SavingTypeFactory(object):
    def create(self, **kwargs):
        data = {
            'id': SavingType.query.count() + 1,
            'name': 'Saving Type 1',
            'active': True
        }
        data.update(kwargs)
        saving_type = SavingType(**data)
        db.session.add(saving_type)
        db.session.commit()
        return saving_type

@pytest.fixture(scope="function")
def saving_type_factory(request):
    return SavingTypeFactory()


class SavingValueFactory(object):
    def create(self, **kwargs):
        saving_type = None
        if not kwargs.get('type_id', None):
            saving_type = SavingTypeFactory().create()

        data = {
            'id': SavingValue.query.count() + 1,
            'value': 100,
            'month': 9,
            'year': 2024,
            'type_id': saving_type.id if saving_type else kwargs['type_id'],
            'used': False
        }
        data.update(kwargs)
        saving_value = SavingValue(**data)
        db.session.add(saving_value)
        db.session.commit()
        return saving_value

@pytest.fixture(scope="function")
def saving_value_factory(request):
    return SavingValueFactory()
