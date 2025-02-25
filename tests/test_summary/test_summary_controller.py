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
        income_type_factory,
        saving_value_factory,
        saving_type_factory,
        user_factory
    ):
        user = user_factory.create()

        expense_type_1 = expense_type_factory.create(
            recurrent=True,
            name='Type 1',
            category=ExpenseCategoryEnum.CARD,
            base_value=100,
            user_id=user.id
        )

        expense_type_2 = expense_type_factory.create(
            recurrent=False,
            name='Type 2',
            category=ExpenseCategoryEnum.CARD,
            base_value=100,
            user_id=user.id
        )
        expense_2 = expense_factory.create(
            type_id=expense_type_2.id,
            month=9,
            year=2024,
            paid=True,
            value=100
        )

        saving_type = saving_type_factory.create(user_id=user.id)
        saving = saving_value_factory.create(
            value=300,
            used=False,
            month=9,
            year=2024,
            type_id=saving_type.id
        )

        income_type = income_type_factory.create(
            name='Salary', 
            recurrent=True,
            user_id=user.id
        )
        income = income_factory.create(
            type_id=income_type.id, 
            value=1000, 
            year=2024, 
            month=9
        )

        expected_expenses_total = expense_type_1.base_value + expense_2.value + saving.value
        expected_incomes_total = income.value
        expected_balance = expected_incomes_total - expected_expenses_total

        result = client.get(
            url_for(SummaryResource.endpoint, year=2024, month=9),
            headers={'x-api-key': user.token}
        )
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
        saving_value_factory,
        saving_type_factory,
        user_factory
    ):
        user = user_factory.create()

        expense_type_factory.create(
            recurrent=True,
            name='Type 1',
            category=ExpenseCategoryEnum.CARD,
            base_value=100,
            user_id=user.id
        )

        expense_type_2 = expense_type_factory.create(
            recurrent=False,
            name='Type 2',
            category=ExpenseCategoryEnum.CARD,
            base_value=100,
            user_id=user.id
        )
        expense_factory.create(
            type_id=expense_type_2.id,
            month=9,
            year=2024,
            paid=True,
            value=100
        )

        saving_type = saving_type_factory.create(user_id=user.id)
        saving_value_factory.create(
            value=300,
            used=False,
            month=9,
            year=2024,
            type_id=saving_type.id
        )

        income_type = income_type_factory.create(
            name='Salary', 
            recurrent=True,
            user_id=user.id
        )
        income_factory.create(
            type_id=income_type.id, 
            value=1000, 
            year=2024, 
            month=9
        )

        result = client.get(
            url_for(SummaryListResource.endpoint, year=2024, month=9),
            headers={'x-api-key': user.token}
        )
        result_json = result.get_json()

        assert result.status_code == 200
        assert len(result_json) == 4
