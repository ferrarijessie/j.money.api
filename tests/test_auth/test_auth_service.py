import pytest

from api.auth.model import User
from api.auth.service import AuthService
from api.auth.exception import (
    UsernameAlreadyExistsException, 
    LoginException, 
    UserNotFoundException
)

class TestAuthService:
    def test_signup(self, client):
        result = AuthService.signup({
            'username': 'ferrarijessie',
            'password': 'password123'
        })

        assert isinstance(result, User)

    def test_signup_error(self, client, user_factory):
        user = user_factory.create()

        with pytest.raises(UsernameAlreadyExistsException):
            AuthService.signup({
                'username': user.username,
                'password': 'password123'
            })

    def test_login_error(self, client, user_factory):
        user = user_factory.create()

        with pytest.raises(LoginException):
            AuthService.login({
                'username': user.username,
                'password': 'password234'
            })

    def test_login_success(self, client, user_factory):
        user = user_factory.create()

        result = AuthService.login({
            'username': user.username,
            'password': 'password123'
        })
        assert result == user

    def test_update_profile_wrong_user(self, client, user_factory):
        user = user_factory.create()

        with pytest.raises(UserNotFoundException):
            AuthService.update_profile(
                {'username': 'new name'},
                user_id=user.id+1
            )

    def test_update_profile_username_already_taken(self, client, user_factory):
        user_1 = user_factory.create()
        user_2 = user_factory.create()

        with pytest.raises(UsernameAlreadyExistsException):
            AuthService.update_profile(
                {'username': user_1.username},
                user_id=user_2.id
            )
    
    def test_update_profile_success(self, client, user_factory):
        user = user_factory.create()

        result = AuthService.update_profile(
            {'username': 'new name'},
            user_id=user.id
        )

        assert result.username == 'new name'
        assert result.id == user.id
