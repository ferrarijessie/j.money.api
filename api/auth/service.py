import uuid

from flask_login import login_user

from database import db

from .exception import UsernameAlreadyExistsException, LoginException, UserNotFoundException
from .model import *
from .interface import CreateUserInterface, UpdateUserInterface


class AuthService:
    @staticmethod
    def signup(data: CreateUserInterface):
        is_username_valid = AuthService._validate_username(data['username'])

        if is_username_valid:
            new_user = User(username=data['username'])
            new_user.password_hash = data['password']
            new_user.token = uuid.uuid4().hex

            db.session.add(new_user)
            db.session.commit()
            
            return new_user
        return None

    @staticmethod
    def login(data: CreateUserInterface):
        user = User.query.filter(User.username == data['username']).first()
        if user.authenticate(data['password']):
            return user
        raise LoginException

    @staticmethod
    def update_profile(data: UpdateUserInterface, user_id: int):
        user = User.query.get(user_id)

        if not user:
            raise UserNotFoundException

        is_username_valid = AuthService._validate_username(data['username'], user_id=user_id)
        if is_username_valid:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.add(user)
            db.session.commit()
            
        return User.query.get(user_id)

    @staticmethod
    def _validate_username(username: str, user_id: int = 0):
        user = User.query.filter(User.username == username).first()
        if user and user.id != user_id:
            raise UsernameAlreadyExistsException
        return True

        
