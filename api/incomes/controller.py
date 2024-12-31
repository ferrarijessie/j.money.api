from flask import request
from flask_restx import Resource, Namespace
from flask_accepts import accepts, responds

from app import api
from ..utils import make_json_response

from .exceptions import (
    IncomeNotFoundException,
    IncomeTypeNotFoundException
)
from .service import IncomeService, IncomeTypeService
from .schema import (
    IncomeCreateSchema,
    IncomeReturnSchema,
    IncomeTypeSchema,
    IncomeTypeReturnSchema,
    IncomeUpdateSchema
)

api = Namespace("Incomes", description="Access to your Incomes")


@api.route('/type')
class IncomeTypeResource(Resource):
    @responds(schema=IncomeTypeReturnSchema(many=True), api=api)
    @api.response(200, "Income types successfully retrieved.")
    def get(self):
        return IncomeTypeService.get_all()

    @accepts(schema=IncomeTypeSchema, api=api)
    @responds(schema=IncomeTypeReturnSchema, api=api)
    @api.response(200, "Income type successfully added.")
    def post(self):
        new_income_type = IncomeTypeService.create(request.parsed_obj)
        return make_json_response(data=IncomeTypeReturnSchema().dump(new_income_type), code=201)

 
@api.route('/type/<int:typeId>')
class IncomeTypeIdResource(Resource):
    @responds(schema=IncomeTypeReturnSchema, api=api)
    @api.response(200, "Income type successfully retrieved.")
    def get(self, typeId):
        try:
            return IncomeTypeService.get_one(typeId)
        except IncomeTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income Type not found"}, code=404)

    @accepts(schema=IncomeTypeSchema, api=api)
    @responds(schema=IncomeTypeReturnSchema, api=api)
    @api.response(200, "Income type successfully added.")
    def put(self, typeId):
        try:
            return IncomeTypeService.update(typeId, data=request.parsed_obj)
        except IncomeTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income Type not found"}, code=404)
   
    @responds(status_code=204, api=api)
    @api.response(204, "Income Type successfully removed.")
    def delete(self, typeId):
        try:
            return IncomeTypeService.delete(typeId)
        except IncomeTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income Type not found"}, code=404)
   

@api.route('/')
class IncomeResource(Resource):
    @responds(schema=IncomeReturnSchema(many=True), api=api)
    @api.response(200, "Incomes successfully retrieved.")
    def get(self):
        return IncomeService.get_all()

    @accepts(schema=IncomeCreateSchema, api=api)
    @responds(schema=IncomeReturnSchema, api=api)
    @api.response(201, "Income successfully added.")
    def post(self):
        new_income = IncomeService.create(data=request.parsed_obj)
        return make_json_response(data=IncomeReturnSchema().dump(new_income), code=201)


@api.route('/<int:incomeId>')
class IncomeIdResource(Resource):
    @responds(schema=IncomeReturnSchema, api=api)
    @api.response(200, "Income successfully retrieved.")
    def get(self, incomeId: int):
        try:
            return IncomeService.get_one(incomeId)
        except IncomeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income not found"}, code=404)

    @accepts(schema=IncomeUpdateSchema, api=api)
    @responds(schema=IncomeReturnSchema, api=api)
    @api.response(201, "Income successfully edited.")
    def put(self, incomeId: int):
        try:
            return IncomeService.update(id=incomeId, data=request.parsed_obj)
        except IncomeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income not found"}, code=404)

    @responds(status_code=204, api=api)
    @api.response(204, "Income successfully removed.")
    def delete(self, incomeId: int):
        try:
            return IncomeService.delete(incomeId)
        except IncomeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Income not found"}, code=404)

 
@api.route('/<int:year>/<int:month>')
class IncomeListResource(Resource):
    @responds(schema=IncomeReturnSchema(many=True), api=api)
    @api.response(200, "Incomes successfully retrieved.")
    def get(self, year, month):
        return IncomeService.get_incomes_list(year=year, month=month)
