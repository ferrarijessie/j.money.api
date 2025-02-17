from flask import url_for

from api.expenses.model import ExpenseCategoryEnum
from api.summary.controller import (
    SummaryResource,
    SummaryListResource
)

class TestSummaryResource:
    def test_get(
        self, 
        client,
        expense_type_factory, 
        expense_factory,
        income_factory, 
        income_type_factory
    ):
        expense_type_1 = expense_type_factory.create(**{
            'recurrent': True, 'name': 'Type 1', 'category': ExpenseCategoryEnum.CARD, 'base_value': 100
        })

        expense_type_2 = expense_type_factory.create(**{
            'recurrent': True, 'name': 'Type 2', 'category': ExpenseCategoryEnum.HOUSE
        })
        expense_2 = expense_factory.create(**{
            'type_id': expense_type_2.id, 'month': 9, 'year': 2024, 'paid': True, 'value': 100
        })

        income_type = income_type_factory.create(**{'name': 'Salary', 'recurrent': True})
        income = income_factory.create(**{
            'type_id': income_type.id, 'value': 300, 'year': 2024, 'month': 9
        })

        expected_expenses_total = expense_type_1.base_value + expense_2.value
        expected_incomes_total = income.value
        expected_balance = expected_incomes_total - expected_expenses_total

        result = client.get(url_for(SummaryResource.endpoint, year=2024, month=9))
        result_json = result.get_json()

        assert result.status_code == 200
        assert result_json['expensesTotal'] == expected_expenses_total
        assert result_json['incomesTotal'] == expected_incomes_total
        assert result_json['balance'] == expected_balance


class TestSummaryListResource:
    def test_get(
        self, 
        client,
        expense_type_factory, 
        expense_factory,
        income_factory, 
        income_type_factory,
        saving_value_factory
    ):
        expense_type_1 = expense_type_factory.create(**{
            'recurrent': True, 'name': 'Type 1', 'category': ExpenseCategoryEnum.CARD, 'base_value': 100
        })

        expense_type_2 = expense_type_factory.create(**{
            'recurrent': True, 'name': 'Type 2', 'category': ExpenseCategoryEnum.HOUSE
        })
        expense_2 = expense_factory.create(**{
            'type_id': expense_type_2.id, 'month': 9, 'year': 2024, 'paid': True, 'value': 100
        })

        income_type = income_type_factory.create(**{'name': 'Salary', 'recurrent': True})
        income = income_factory.create(**{
            'type_id': income_type.id, 'value': 300, 'year': 2024, 'month': 9
        })

        saving = saving_value_factory.create(**{
            'value': 300,
            'used': False,
            'month': 9,
            'year': 2024
        })

        result = client.get(url_for(SummaryListResource.endpoint, year=2024, month=9))
        result_json = result.get_json()

        assert result.status_code == 200
        assert len(result_json) == 4
