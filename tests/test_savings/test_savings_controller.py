from flask import url_for

from api.savings.controller import (
    SavingTypeResource,
    SavingTypeIdResource,
    SavingValueResource,
    SavingValueIdResource,
    SavingSummaryResource
)


class TestSavingTypeResource:
    def test_get_empty_result(self, client, user_factory):
        user = user_factory.create()

        response = client.get(
            url_for(SavingTypeResource.endpoint),
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 200
        assert response.get_json() == []

    
    def test_get_with_result(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()

        response = client.get(
            url_for(SavingTypeResource.endpoint),
            headers={'x-api-key': saving_type.user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert len(response_json) == 1
        assert response_json[0]["id"] == saving_type.id

    def test_post(self, client, user_factory):
        user = user_factory.create()

        payload = {
            'name': 'New Saving Type',
            'active': True
        }

        response = client.post(
            url_for(SavingTypeResource.endpoint), 
            json=payload,
            headers={'x-api-key': user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 201
        assert response_json["name"] == 'New Saving Type'
        assert response_json["active"] == True


class TestSavingTypeIdResource:
    def test_get_empty_result(self, client, user_factory):
        user = user_factory.create()

        response = client.get(
            url_for(SavingTypeIdResource.endpoint, typeId=1),
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Saving Type not found'}

    def test_get_with_result(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()

        response = client.get(
            url_for(SavingTypeIdResource.endpoint, typeId=saving_type.id),
            headers={'x-api-key': saving_type.user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert response_json["id"] == saving_type.id
        assert response_json["name"] == saving_type.name
        assert response_json["active"] == saving_type.active

    def test_put_non_existent(self, client, user_factory):
        user = user_factory.create()

        payload = {
            "name": 'Edited Saving Type',
            "active": True
        }

        response = client.put(
            url_for(SavingTypeIdResource.endpoint, typeId=1),
            json=payload,
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Saving Type not found'}

    def test_put_success(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()
        payload = {
            "name": 'Edited Saving Type',
            "active": False
        }

        response = client.put(
            url_for(SavingTypeIdResource.endpoint, typeId=saving_type.id),
            json=payload,
            headers={'x-api-key': saving_type.user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert response_json["name"] == 'Edited Saving Type'
        assert response_json["active"] == False

    def test_delete_non_existent(self, client, user_factory):
        user = user_factory.create()

        response = client.delete(
            url_for(SavingTypeIdResource.endpoint, typeId=1),
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Saving Type not found'}

    def test_delete_non_existent(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()

        response = client.delete(
            url_for(SavingTypeIdResource.endpoint, typeId=saving_type.id),
            headers={'x-api-key': saving_type.user.token}
        )

        assert response.status_code == 204


class TestSavingValueResource:
    def test_get_empty_result(self, client, user_factory):
        user = user_factory.create()

        response = client.get(
            url_for(SavingValueResource.endpoint),
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 200
        assert response.get_json() == []

    
    def test_get_with_result(self, client, saving_value_factory):
        saving_value = saving_value_factory.create()

        response = client.get(
            url_for(SavingValueResource.endpoint),
            headers={'x-api-key': saving_value.user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert len(response_json) == 1
        assert response_json[0]["id"] == saving_value.id

    def test_post(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()
        payload = {
            'value': 100,
            'month': 9,
            'year': 2024,
            'typeId': saving_type.id,
            'used': False
        }

        response = client.post(
            url_for(SavingValueResource.endpoint), 
            json=payload,
            headers={'x-api-key': saving_type.user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 201
        assert response_json["id"] > 0
        assert response_json["value"] == 100
        assert response_json["month"] == 9
        assert response_json["year"] == 2024
        assert response_json["typeId"] == saving_type.id
        assert response_json["used"] == False


class TestSavingValueIdResource:
    def test_get_empty_result(self, client, user_factory):
        user = user_factory.create()

        response = client.get(
            url_for(SavingValueIdResource.endpoint, id=1),
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Saving Value not found'}

    def test_get_with_result(self, client, saving_value_factory):
        saving_value = saving_value_factory.create()

        response = client.get(
            url_for(SavingValueIdResource.endpoint, id=saving_value.id),
            headers={'x-api-key': saving_value.user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert response_json["id"] == saving_value.id
        assert response_json["value"] == saving_value.value
        assert response_json["month"] == saving_value.month
        assert response_json["year"] == saving_value.year
        assert response_json["typeId"] == saving_value.type_id
        assert response_json["used"] == saving_value.used

    def test_put_non_existent(self, client, user_factory):
        user = user_factory.create()

        payload = {
            "value": 500,
            "used": True
        }

        response = client.put(
            url_for(SavingValueIdResource.endpoint, id=1),
            json=payload,
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Saving Value not found'}

    def test_put_success(self, client, saving_value_factory):
        saving_value = saving_value_factory.create()
        payload = {
            "value": 500,
            "used": True
        }

        response = client.put(
            url_for(SavingValueIdResource.endpoint, id=saving_value.id),
            json=payload,
            headers={'x-api-key': saving_value.user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert response_json["value"] == 500
        assert response_json["used"] == True

    def test_delete_non_existent(self, client, user_factory):
        user = user_factory.create()

        response = client.delete(
            url_for(SavingValueIdResource.endpoint, id=1),
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 404
        assert response.get_json() == {'code': 404, 'message': 'Saving Value not found'}

    def test_delete_non_existent(self, client, saving_value_factory):
        saving_value = saving_value_factory.create()

        response = client.delete(
            url_for(SavingValueIdResource.endpoint, id=saving_value.id),
            headers={'x-api-key': saving_value.user.token}
        )

        assert response.status_code == 204


class TestSavingSummaryResource:
    def test_get_empty_result(self, client, user_factory):
        user = user_factory.create()

        response = client.get(
            url_for(SavingSummaryResource.endpoint, year=2024, month=9),
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 200
        assert response.get_json() == []

    
    def test_get_with_result(self, client, saving_type_factory, saving_value_factory, user_factory):
        user = user_factory.create()
        saving_type_1 = saving_type_factory.create(user_id=user.id)
        saving_type_2 = saving_type_factory.create(user_id=user.id)
        saving_value_factory.create(month=9, year=2024, type_id=saving_type_1.id)
        saving_value_factory.create(month=9, year=2024, type_id=saving_type_2.id)

        response = client.get(
            url_for(SavingSummaryResource.endpoint, year=2024, month=9),
            headers={'x-api-key': user.token}
        )
        response_json = response.get_json()

        assert response.status_code == 200
        assert len(response_json) == 2
