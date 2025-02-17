from mock import patch, Mock

from api.expenses.model import ExpenseCategoryEnum

from api.summary.service import (
    SummaryService
)


class TestSummaryService:
    def test_get_summary_success(
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

        saving = saving_value_factory.create(**{
            'value': 300,
            'used': False,
            'month': 9,
            'year': 2024
        })

        income_type = income_type_factory.create(**{'name': 'Salary', 'recurrent': True})
        income = income_factory.create(**{
            'type_id': income_type.id, 'value': 1000, 'year': 2024, 'month': 9
        })

        expected_expenses_total = expense_type_1.base_value + expense_2.value + saving.value
        expected_incomes_total = income.value
        expected_balance = expected_incomes_total - expected_expenses_total

        result = SummaryService.get_summary(year=2024, month=9)

        assert result['expenses_total'] == expected_expenses_total
        assert result['incomes_total'] == expected_incomes_total
        assert result['balance'] == expected_balance

    def test_get_summary_list(
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

        saving = saving_value_factory.create(**{
            'value': 300,
            'used': False,
            'month': 9,
            'year': 2024
        })

        income_type = income_type_factory.create(**{'name': 'Salary', 'recurrent': True})
        income = income_factory.create(**{
            'type_id': income_type.id, 'value': 1000, 'year': 2024, 'month': 9
        })

        result = SummaryService.get_summary_list(year=2024, month=9)

        assert len(result) == 4
