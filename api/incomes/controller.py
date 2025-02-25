from flask import request
from flask_restx import Resource, Namespace
from flask_accepts import accepts, responds
from flask_login import login_required, current_user

from app import api
from ..utils import make_json_response

from .exceptions import (
    IncomeNotFoundException,
    IncomeTypeNotFoundException
)
from .service import IncomeService, IncomeTypeService
from .schema import (
    IncomeInputSchema,
    IncomeReturnSchema,
    IncomeTypeSchema,
    IncomeTypeReturnSchema,
)

api = Namespace("Incomes", description="Access to your Incomes")


@api.route('/type')
class IncomeTypeResource(Resource):
    @responds(schema=IncomeTypeReturnSchema(many=True), api=api)
    @api.response(200, "Income types successfully retrieved.")
    @login_required
    def get(self):
        user_id = current_user.id
        return IncomeTypeService.get_all(user_id=user_id)

    @accepts(schema=IncomeTypeSchema, api=api)
    @responds(schema=IncomeTypeReturnSchema, api=api)
    @api.response(200, "Income type successfully added.")
    @login_required
    def post(self):
        user_id = current_user.id
        data = request.parsed_obj
        data['user_id'] = user_id
        new_income_type = IncomeTypeService.create(data)
        return make_json_response(data=IncomeTypeReturnSchema().dump(new_income_type), code=201)

 
@api.route('/type/<int:typeId>')
class IncomeTypeIdResource(Resource):
    @responds(schema=IncomeTypeReturnSchema, api=api)
    @api.response(200, "Income type successfully retrieved.")
    @login_required
    def get(self, typeId):
        user_id = current_user.id
        try:
            return IncomeTypeService.get_one(typeId, user_id=user_id)
        except IncomeTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income Type not found"}, code=404)

    @accepts(schema=IncomeTypeSchema, api=api)
    @responds(schema=IncomeTypeReturnSchema, api=api)
    @api.response(200, "Income type successfully added.")
    @login_required
    def put(self, typeId):
        user_id = current_user.id
        try:
            return IncomeTypeService.update(typeId, data=request.parsed_obj, user_id=user_id)
        except IncomeTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income Type not found"}, code=404)
   
    @responds(status_code=204, api=api)
    @api.response(204, "Income Type successfully removed.")
    @login_required
    def delete(self, typeId):
        user_id = current_user.id
        try:
            return IncomeTypeService.delete(typeId, user_id=user_id)
        except IncomeTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income Type not found"}, code=404)
   

@api.route('/')
class IncomeResource(Resource):
    @responds(schema=IncomeReturnSchema(many=True), api=api)
    @api.response(200, "Incomes successfully retrieved.")
    @login_required
    def get(self):
        user_id = current_user.id
        return IncomeService.get_all(user_id=user_id)

    @accepts(schema=IncomeInputSchema, api=api)
    @responds(schema=IncomeReturnSchema, api=api)
    @api.response(201, "Income successfully added.")
    @login_required
    def post(self):
        new_income = IncomeService.create(data=request.parsed_obj)
        return make_json_response(data=IncomeReturnSchema().dump(new_income), code=201)


@api.route('/<int:incomeId>')
class IncomeIdResource(Resource):
    @responds(schema=IncomeReturnSchema, api=api)
    @api.response(200, "Income successfully retrieved.")
    @login_required
    def get(self, incomeId: int):
        user_id = current_user.id
        try:
            return IncomeService.get_one(incomeId, user_id=user_id)
        except IncomeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income not found"}, code=404)

    @accepts(schema=IncomeInputSchema, api=api)
    @responds(schema=IncomeReturnSchema, api=api)
    @api.response(201, "Income successfully edited.")
    @login_required
    def put(self, incomeId: int):
        user_id = current_user.id
        try:
            return IncomeService.update(id=incomeId, data=request.parsed_obj, user_id=user_id)
        except IncomeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income not found"}, code=404)

    @responds(status_code=204, api=api)
    @api.response(204, "Income successfully removed.")
    @login_required
    def delete(self, incomeId: int):
        user_id = current_user.id
        try:
            return IncomeService.delete(incomeId, user_id=user_id)
        except IncomeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income not found"}, code=404)

 
@api.route('/<int:year>/<int:month>')
class IncomeListResource(Resource):
    @responds(schema=IncomeReturnSchema(many=True), api=api)
    @api.response(200, "Incomes successfully retrieved.")
    @login_required
    def get(self, year, month):
        user_id = current_user.id
        return IncomeService.get_incomes_list(year=year, month=month, user_id=user_id)
