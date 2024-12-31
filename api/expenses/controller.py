from flask import request
from flask_restx import Resource, Namespace
from flask_accepts import accepts, responds

from app import api
from ..utils import make_json_response

from .exceptions import (
    ExpenseNotFoundException,
    ExpenseTypeNotFoundException,
)
from .service import (
    ExpenseTypeService, 
    ExpenseService,
)
from .schema import (
    ExpenseTypeReturnSchema, 
    ExpenseTypeAcceptSchema,
    ExpenseCreateSchema,
    ExpenseReturnSchema,
    ExpenseListReturnSchema,
    ExpenseUpdateSchema,
)

api = Namespace("Expenses", description="Access to your Expenses")




@api.route('/')
class ExpenseResource(Resource):
    @responds(schema=ExpenseReturnSchema(many=True), api=api)
    @api.response(200, "Expenses successfully retrieved.")
    def get(self):
        return ExpenseService.get_all()

    @accepts(schema=ExpenseCreateSchema, api=api)
    @responds(schema=ExpenseReturnSchema, api=api)
    @api.response(200, "Expense successfully added.")
    def post(self):
        new_expense = ExpenseService.create(data=request.parsed_obj)
        return make_json_response(data=ExpenseReturnSchema().dump(new_expense), code=201)


@api.route('/<int:expenseId>')
class ExpenseIdResource(Resource):
    @responds(schema=ExpenseReturnSchema, api=api)
    @api.response(200, "Expense successfully retrieved.")
    def get(self, expenseId: int):
        try:
            return ExpenseService.get_one(expenseId)
        except ExpenseNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense not found"}, code=404)

    @accepts(schema=ExpenseUpdateSchema, api=api)
    @responds(schema=ExpenseReturnSchema, api=api)
    @api.response(201, "Expense successfully edited.")
    def put(self, expenseId: int):
        try:
            return ExpenseService.update(id=expenseId, data=request.parsed_obj)
        except ExpenseNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense not found"}, code=404)

    @responds(status_code=204, api=api)
    @api.response(204, "Expense successfully removed.")
    def delete(self, expenseId: int):
        try:
            return ExpenseService.delete(expenseId)
        except ExpenseNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense not found"}, code=404)


@api.route('/<string:category>')
class ExpenseByCategoryResource(Resource):
    @responds(schema=ExpenseReturnSchema(many=True), api=api)
    @api.response(200, "Expenses successfully retrieved.")
    def get(self, category: str):
        return ExpenseService.get_by_category(category)


@api.route('/<string:category>/<int:year>/<int:month>')
class ExpenseListResource(Resource):
    @responds(schema=ExpenseListReturnSchema(many=True), api=api)
    @api.response(200, "Expenses successfully retrieved.")
    def get(self, category: str, year: int, month: int):
        return ExpenseService.get_expense_list(category=category, year=year, month=month)
 

@api.route('/type')
class ExpenseTypeResource(Resource):
    @responds(schema=ExpenseTypeReturnSchema(many=True), api=api)
    @api.response(200, "Expense types successfully retrieved.")
    def get(self):
        return ExpenseTypeService.get_all()

    @accepts(schema=ExpenseTypeAcceptSchema, api=api)
    @responds(schema=ExpenseTypeReturnSchema, api=api)
    @api.response(200, "Expense type successfully added.")
    def post(self):
        new_expense_type = ExpenseTypeService.create(request.parsed_obj)
        return make_json_response(data=ExpenseTypeReturnSchema().dump(new_expense_type), code=201)


@api.route('/type/<int:typeId>')
class ExpenseTypeIdResource(Resource):
    @responds(schema=ExpenseTypeReturnSchema, api=api)
    @api.response(200, "Expense type successfully retrieved.")
    def get(self, typeId):
        try:
            return ExpenseTypeService.get_one(typeId)
        except ExpenseTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense Type not found"}, code=404)

    @accepts(schema=ExpenseTypeAcceptSchema, api=api)
    @responds(schema=ExpenseTypeReturnSchema, api=api)
    @api.response(200, "Expense type successfully added.")
    def put(self, typeId):
        try:
            return ExpenseTypeService.update(typeId, request.parsed_obj)
        except ExpenseTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense Type not found"}, code=404)

    @responds(status_code=204, api=api)
    @api.response(200, "Expense type successfully deleted.")
    def delete(self, typeId):
        try:
            return ExpenseTypeService.delete(typeId)
        except ExpenseTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense Type not found"}, code=404)
