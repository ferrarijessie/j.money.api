from flask import request
from flask_restx import Resource, Namespace
from flask_accepts import accepts, responds
from flask_login import login_user, current_user, login_required

from app import api
from ..utils import make_json_response

from .schema import UserSchema, UserUpdateSchema
from .service import AuthService


api = Namespace("Auth", description="Access to Auth")


@api.route('/signup')
class SignupResource(Resource):
    @accepts(schema=UserSchema, api=api)
    @responds(schema=UserSchema, api=api)
    @api.response(200, "User successfully created.")
    def post(self):
        return AuthService.signup(request.parsed_obj)
    
@api.route('/user')
class UserResource(Resource):
    @accepts(schema=UserUpdateSchema, api=api)
    @responds(schema=UserSchema, api=api)
    @api.response(200, "User successfully updated.")
    @login_required
    def put(self):
        user_id = current_user.id
        return AuthService.update_profile(request.parsed_obj, user_id=user_id)



@api.route('/login')
class UserLoginResource(Resource):
    @accepts(schema=UserSchema, api=api)
    @responds(schema=UserSchema, api=api)
    @api.response(200, "Logged in")
    def post(self):
        try:
            user = AuthService.login(request.parsed_obj)
            login_user(user)
            return user
        except Exception as e:
            return make_json_response(
                data={'message': f'{e}', 'code': 401}, code=401)
