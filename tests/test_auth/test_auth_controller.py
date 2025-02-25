from flask import url_for

from api.auth.controller import (
    UserResource,
    UserLoginResource
)

class TestUserResource:
    def test_post_success(self, client):
        payload = {
            'username': 'ferrarijessie',
            'password': 'password123'
        }

        response = client.post(
            url_for(UserResource.endpoint),
            json=payload
        )

        assert response.status_code == 200
        assert response.get_json()['username'] == 'ferrarijessie'

    def test_put_success(self, client, user_factory):
        user = user_factory.create()
        payload = {
            'username': 'ferrarijessie'
        }

        response = client.put(
            url_for(UserResource.endpoint),
            json=payload,
            headers={'x-api-key': user.token}
        )

        assert response.status_code == 200
        assert response.get_json()['username'] == 'ferrarijessie'


class TestLoginResource:
    def test_post_wrong_password(self, client, user_factory):
        user = user_factory.create()

        payload = {
            'username': user.username,
            'password': '123456'
        }

        response = client.post(
            url_for(UserLoginResource.endpoint),
            json=payload
        )

        assert response.status_code == 401

