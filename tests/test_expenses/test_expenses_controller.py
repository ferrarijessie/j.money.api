from flask import url_for

from api.expenses.controller import (
    ExpenseResource,
    ExpenseIdResource,
    ExpenseByCategoryResource,
    ExpenseListResource,
    ExpenseTypeResource,
    ExpenseTypeIdResource,
)
from api.expenses.model import ExpenseCategoryEnum

class TestExpenseResource:
    def test_get_empty_result(self, client):
        response = client.get(
            url_for(ExpenseResource.endpoint)
        )

        assert response.status_code == 200
        assert response.get_json() == []

    
    def test_get_with_result(self, client, expense_factory):
        expense = expense_factory.create()

        response = client.get(
            url_for(ExpenseResource.endpoint)
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert len(response_json) == 1
        assert response_json[0]["expenseId"] == expense.id

    def test_post(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()
        payload = {
            'value': 100,
            'month': 1,
            'year': 2024,
            'typeId': expense_type.id,
        }

        response = client.post(
            url_for(ExpenseResource.endpoint), 
            json=payload
        )
        response_json = response.get_json()

        assert response.status_code == 201
        assert response_json["expenseId"] > 0
        assert response_json["value"] == 100
        assert response_json["month"] == 1
        assert response_json["year"] == 2024
        assert response_json["typeId"] == expense_type.id
        assert response_json["paid"] == False


class TestExpenseIdResource:
    def test_get_empty_result(self, client):
        response = client.get(
            url_for(ExpenseIdResource.endpoint, expenseId=1)
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Expense not found'}

    def test_get_with_result(self, client, expense_factory):
        expense = expense_factory.create()

        response = client.get(
            url_for(ExpenseIdResource.endpoint, expenseId=expense.id)
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert response_json["expenseId"] == expense.id
        assert response_json["value"] == expense.value
        assert response_json["month"] == expense.month
        assert response_json["year"] == expense.year
        assert response_json["typeId"] == expense.type_id
        assert response_json["paid"] == expense.paid

    def test_put_non_existent(self, client):
        payload = {
            "value": 123,
            "paid": True
        }

        response = client.put(
            url_for(ExpenseIdResource.endpoint, expenseId=1),
            json=payload
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Expense not found'}

    def test_put_success(self, client, expense_factory):
        expense = expense_factory.create()
        payload = {
            "value": 123,
            "paid": True
        }

        response = client.put(
            url_for(ExpenseIdResource.endpoint, expenseId=expense.id),
            json=payload
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert response_json["value"] == 123
        assert response_json["paid"] == True

    def test_delete_non_existent(self, client):
        response = client.delete(
            url_for(ExpenseIdResource.endpoint, expenseId=1)
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Expense not found'}

    def test_delete_non_existent(self, client, expense_factory):
        expense = expense_factory.create()

        response = client.delete(
            url_for(ExpenseIdResource.endpoint, expenseId=expense.id)
        )

        assert response.status_code == 204


class TestExpenseByCategoryResource:
    def test_get_empty_result(self, client):
        response = client.get(
            url_for(ExpenseByCategoryResource.endpoint, category="personal")
        )

        assert response.status_code == 200
        assert response.get_json() == []

    
    def test_get_with_result(self, client, expense_factory):
        expense = expense_factory.create()

        response = client.get(
            url_for(ExpenseByCategoryResource.endpoint, category=expense.expense_type.category.value)
        )
        response_json = response.get_json()[0]

        assert response.status_code == 200
        assert response_json["expenseId"] == expense.id


class TestExpenseListResource:
    def test_empty_result(self, client):
        response = client.get(
            url_for(ExpenseListResource.endpoint, category="personal", month=9, year=2024)
        )

        assert response.status_code == 200
        assert response.get_json() == []

    def test_with_result(
        self,
        client, 
        expense_type_factory, 
        expense_factory
    ):
        expense_type_1 = expense_type_factory.create(**{'recurrent': True, 'name': 'Type 1', 'base_value': 100})

        expense_type_2 = expense_type_factory.create(**{'recurrent': True, 'name': 'Type 2'})
        expense_factory.create(**{'type_id': expense_type_2.id, 'month': 9, 'year': 2024, 'paid': True})

        response = client.get(
            url_for(ExpenseListResource.endpoint, category=expense_type_1.category.value, month=9, year=2024)
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert len(response_json) == 2


class TestExpenseTypeResource:
    def test_get_empty_result(self, client):
        response = client.get(
            url_for(ExpenseTypeResource.endpoint)
        )

        assert response.status_code == 200
        assert response.get_json() == []

    def test_get_with_result(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()

        response = client.get(
            url_for(ExpenseTypeResource.endpoint)
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert response_json[0]["expenseTypeId"] == expense_type.id

    def test_post_success(self, client):
        payload = {
            'name': 'Luz',
            'category': ExpenseCategoryEnum.HOUSE.value,
            'recurrent': True
        }

        response = client.post(
            url_for(ExpenseTypeResource.endpoint),
            json=payload
        )
        response_json = response.get_json()

        assert response.status_code == 201
        assert response_json["expenseTypeId"] > 0
        assert response_json["name"] == "Luz"
        assert response_json["category"] == ExpenseCategoryEnum.HOUSE.value
        assert response_json["recurrent"] == True


class TestExpenseTypeIdResource:
    def test_get_non_existent(self, client):
        response = client.get(
            url_for(ExpenseTypeIdResource.endpoint, typeId=1)
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Expense Type not found'}

    def test_get_success(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()

        response = client.get(
            url_for(ExpenseTypeIdResource.endpoint, typeId=expense_type.id)
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert response_json["expenseTypeId"] == expense_type.id

    def test_put_non_existent(self, client):
        payload = {
            "name": "New Type",
            "category": ExpenseCategoryEnum.HEALTH.value,
            "recurrent": True
        }

        response = client.put(
            url_for(ExpenseTypeIdResource.endpoint, typeId=1),
            json=payload
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Expense Type not found'}

    def test_put_success(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()
        payload = {
            "name": "New Type",
            "category": ExpenseCategoryEnum.HEALTH.value,
            "recurrent": True
        }

        response = client.put(
            url_for(ExpenseTypeIdResource.endpoint, typeId=expense_type.id),
            json=payload
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert response_json["expenseTypeId"] == expense_type.id
        assert response_json["name"] == "New Type"
        assert response_json["category"] == ExpenseCategoryEnum.HEALTH.value
        assert response_json["recurrent"] == True

    def test_delete_non_existent(self, client):
        response = client.delete(
            url_for(ExpenseTypeIdResource.endpoint, typeId=1),
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Expense Type not found'}

    def test_delete_success(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()

        response = client.delete(
            url_for(ExpenseTypeIdResource.endpoint, typeId=expense_type.id),
        )

        assert response.status_code == 204
