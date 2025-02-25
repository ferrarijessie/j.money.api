from flask import url_for

from api.incomes.controller import (
    IncomeTypeResource,
    IncomeTypeIdResource,
    IncomeResource,
    IncomeIdResource,
    IncomeListResource
)


class TestIncomeTypeResource:
    def test_get_empty_result(self, client, user_factory):
        user = user_factory.create()

        result = client.get(
            url_for(IncomeTypeResource.endpoint),
            headers={'x-api-key': user.token}
        )

        assert result.status_code == 200
        assert result.get_json() == []

    def test_get_with_result(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = client.get(
            url_for(IncomeTypeResource.endpoint),
            headers={'x-api-key': income_type.user.token}
        )

        assert result.status_code == 200
        assert len(result.get_json()) > 0
        assert result.get_json()[0]['incomeTypeId'] == income_type.id

    def test_post_success(self, client, user_factory):
        user = user_factory.create()

        payload = {
            'name': 'New Income Type'
        }

        result = client.post(
            url_for(IncomeTypeResource.endpoint),
            json=payload,
            headers={'x-api-key': user.token}
        )
        result_json = result.get_json()

        assert result.status_code == 201
        assert result_json['incomeTypeId'] > 0
        assert result_json['name'] == 'New Income Type'
        assert result_json['recurrent'] == False


class  TestIncomeTypeIdResource:
    def test_get_empty_result(self, client, user_factory):
        user = user_factory.create()

        result = client.get(
            url_for(IncomeTypeIdResource.endpoint, typeId=1),
            headers={'x-api-key': user.token}
        )

        assert result.status_code == 404
        assert result.get_json() == {"code": 404, "message": "Income Type not found"}

    def test_get_with_result(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = client.get(
            url_for(IncomeTypeIdResource.endpoint, typeId=income_type.id),
            headers={'x-api-key': income_type.user.token}
        )

        assert result.status_code == 200
        assert result.get_json()['incomeTypeId'] == income_type.id

    def test_put_non_existent(self, client, user_factory):
        user = user_factory.create()

        payload = {
            'name': 'New Income Type',
            'recurrent': True
        }

        result = client.put(
            url_for(IncomeTypeIdResource.endpoint, typeId=1),
            json=payload,
            headers={'x-api-key': user.token}
        )

        assert result.status_code == 404
        assert result.get_json() == {"code": 404, "message": "Income Type not found"}

    def test_put_success(self, client, income_type_factory):
        income_type = income_type_factory.create()
        payload = {
            'name': 'Edited Income Type',
            'recurrent': True
        }

        result = client.put(
            url_for(IncomeTypeIdResource.endpoint, typeId=income_type.id),
            json=payload,
            headers={'x-api-key': income_type.user.token}
        )

        assert result.status_code == 200
        assert result.get_json()['incomeTypeId'] == income_type.id
        assert result.get_json()['name'] == 'Edited Income Type'
        assert result.get_json()['recurrent'] == True

    def test_delete_non_existent(self, client, user_factory):
        user = user_factory.create()

        result = client.delete(
            url_for(IncomeTypeIdResource.endpoint, typeId=1),
            headers={'x-api-key': user.token}
        )

        assert result.status_code == 404
        assert result.get_json() == {"code": 404, "message": "Income Type not found"}

    def test_delete_success(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = client.delete(
            url_for(IncomeTypeIdResource.endpoint, typeId=income_type.id),
            headers={'x-api-key': income_type.user.token}
        )

        assert result.status_code == 204


class TestIncomeResource:
    def test_get_empty_result(self, client, user_factory):
        user = user_factory.create()

        result = client.get(
            url_for(IncomeResource.endpoint),
            headers={'x-api-key': user.token}
        )

        assert result.status_code == 200
        assert result.get_json() == []

    def test_get_with_result(self, client, income_factory):
        income = income_factory.create()

        result = client.get(
            url_for(IncomeResource.endpoint),
            headers={'x-api-key': income.user.token}
        )

        assert result.status_code == 200
        assert result.get_json()[0]['id'] == income.id

    def test_post_success(self, client, income_type_factory):
        income_type = income_type_factory.create()

        payload = {
            'typeId': income_type.id,
            'value': 123,
            'month': 9,
            'year': 2024
        }

        result = client.post(
            url_for(IncomeResource.endpoint),
            json=payload,
            headers={'x-api-key': income_type.user.token}
        )
        result_json = result.get_json()

        assert result.status_code == 201
        assert result_json['id'] > 0
        assert result_json['typeId'] == income_type.id
        assert result_json['value'] == 123
        assert result_json['month'] == 9
        assert result_json['year'] == 2024
        assert result_json['received'] == False


class  TestIncomeIdResource:
    def test_get_empty_result(self, client, user_factory):
        user = user_factory.create()

        result = client.get(
            url_for(IncomeIdResource.endpoint, incomeId=1),
            headers={'x-api-key': user.token}
        )

        assert result.status_code == 404
        assert result.get_json() == {"code": 404, "message": "Income not found"}

    def test_get_with_result(self, client, income_factory):
        income = income_factory.create()

        result = client.get(
            url_for(IncomeIdResource.endpoint, incomeId=income.id),
            headers={'x-api-key': income.user.token}
        )

        assert result.status_code == 200
        assert result.get_json()['id'] == income.id

    def test_put_non_existent(self, client, user_factory):
        user = user_factory.create()

        payload = {
            'value': 321,
            'received': True
        }

        result = client.put(
            url_for(IncomeIdResource.endpoint, incomeId=1),
            json=payload,
            headers={'x-api-key': user.token}
        )

        assert result.status_code == 404
        assert result.get_json() == {"code": 404, "message": "Income not found"}

    def test_put_success(self, client, income_factory):
        income = income_factory.create()
        payload = {
            'value': 321,
            'received': True
        }

        result = client.put(
            url_for(IncomeIdResource.endpoint, incomeId=income.id),
            json=payload,
            headers={'x-api-key': income.user.token}
        )
        result_json = result.get_json()

        assert result.status_code == 200
        assert result_json['id'] == income.id
        assert result_json['value'] == 321
        assert result_json['received'] == True

    def test_delete_non_existent(self, client, user_factory):
        user = user_factory.create()

        result = client.delete(
            url_for(IncomeIdResource.endpoint, incomeId=1),
            headers={'x-api-key': user.token}
        )

        assert result.status_code == 404
        assert result.get_json() == {"code": 404, "message": "Income not found"}

    def test_delete_success(self, client, income_factory):
        income = income_factory.create()

        result = client.delete(
            url_for(IncomeIdResource.endpoint, incomeId=income.id),
            headers={'x-api-key': income.user.token}
        )

        assert result.status_code == 204


class TestIncomeListResource:
    def test_with_result(
        self,
        client,
        income_type_factory, 
        income_factory,
        user_factory
    ):
        user = user_factory.create()

        income_type_factory.create(name='Salary', recurrent=True, user_id=user.id)

        income_type_2 = income_type_factory.create(name='Salary', recurrent=True, user_id=user.id)
        income_factory.create(type_id=income_type_2.id, value=100, year=2024, month=9)

        response = client.get(
            url_for(IncomeListResource.endpoint, month=9, year=2024),
            headers={'x-api-key': user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert len(response_json) == 2
