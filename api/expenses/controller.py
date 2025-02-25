from flask import request
from flask_restx import Resource, Namespace
from flask_accepts import accepts, responds
from flask_login import login_required, current_user

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
    ExpenseInputSchema,
    ExpenseReturnSchema,
)

api = Namespace("Expenses", description="Access to your Expenses")




@api.route('/')
class ExpenseResource(Resource):
    @responds(schema=ExpenseReturnSchema(many=True), api=api)
    @api.response(200, "Expenses successfully retrieved.")
    @login_required
    def get(self):
        user_id = current_user.id
        return ExpenseService.get_all(user_id=user_id)

    @accepts(schema=ExpenseInputSchema, api=api)
    @responds(schema=ExpenseReturnSchema, api=api)
    @api.response(200, "Expense successfully added.")
    @login_required
    def post(self):
        new_expense = ExpenseService.create(data=request.parsed_obj)
        return make_json_response(data=ExpenseReturnSchema().dump(new_expense), code=201)


@api.route('/<int:expenseId>')
class ExpenseIdResource(Resource):
    @responds(schema=ExpenseReturnSchema, api=api)
    @api.response(200, "Expense successfully retrieved.")
    @login_required
    def get(self, expenseId: int):
        user_id = current_user.id
        try:
            return ExpenseService.get_one(expenseId, user_id=user_id)
        except ExpenseNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense not found"}, code=404)

    @accepts(schema=ExpenseInputSchema, api=api)
    @responds(schema=ExpenseReturnSchema, api=api)
    @api.response(201, "Expense successfully edited.")
    @login_required
    def put(self, expenseId: int):
        user_id = current_user.id
        try:
            return ExpenseService.update(id=expenseId, data=request.parsed_obj, user_id=user_id)
        except ExpenseNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense not found"}, code=404)

    @responds(status_code=204, api=api)
    @api.response(204, "Expense successfully removed.")
    @login_required
    def delete(self, expenseId: int):
        user_id = current_user.id
        try:
            return ExpenseService.delete(expenseId, user_id=user_id)
        except ExpenseNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense not found"}, code=404)


@api.route('/<string:category>')
class ExpenseByCategoryResource(Resource):
    @responds(schema=ExpenseReturnSchema(many=True), api=api)
    @api.response(200, "Expenses successfully retrieved.")
    @login_required
    def get(self, category: str):
        user_id = current_user.id
        return ExpenseService.get_by_category(category, user_id=user_id)


@api.route('/<string:category>/<int:year>/<int:month>')
class ExpenseListResource(Resource):
    @responds(schema=ExpenseReturnSchema(many=True), api=api)
    @api.response(200, "Expenses successfully retrieved.")
    @login_required
    def get(self, category: str, year: int, month: int):
        user_id = current_user.id
        return ExpenseService.get_expense_list(category=category, year=year, month=month, user_id=user_id)
 

@api.route('/type')
class ExpenseTypeResource(Resource):
    @responds(schema=ExpenseTypeReturnSchema(many=True), api=api)
    @api.response(200, "Expense types successfully retrieved.")
    @login_required
    def get(self):
        user_id = current_user.id
        return ExpenseTypeService.get_all(user_id=user_id)

    @accepts(schema=ExpenseTypeAcceptSchema, api=api)
    @responds(schema=ExpenseTypeReturnSchema, api=api)
    @api.response(200, "Expense type successfully added.")
    @login_required
    def post(self):
        user_id = current_user.id
        data = request.parsed_obj
        data['user_id'] = user_id
        new_expense_type = ExpenseTypeService.create(data)
        return make_json_response(data=ExpenseTypeReturnSchema().dump(new_expense_type), code=201)


@api.route('/type/<int:typeId>')
class ExpenseTypeIdResource(Resource):
    @responds(schema=ExpenseTypeReturnSchema, api=api)
    @api.response(200, "Expense type successfully retrieved.")
    @login_required
    def get(self, typeId):
        user_id = current_user.id
        try:
            return ExpenseTypeService.get_one(typeId, user_id=user_id)
        except ExpenseTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense Type not found"}, code=404)

    @accepts(schema=ExpenseTypeAcceptSchema, api=api)
    @responds(schema=ExpenseTypeReturnSchema, api=api)
    @api.response(200, "Expense type successfully added.")
    @login_required
    def put(self, typeId):
        user_id = current_user.id
        try:
            return ExpenseTypeService.update(typeId, request.parsed_obj, user_id=user_id)
        except ExpenseTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense Type not found"}, code=404)

    @responds(status_code=204, api=api)
    @api.response(200, "Expense type successfully deleted.")
    @login_required
    def delete(self, typeId):
        user_id = current_user.id
        try:
            return ExpenseTypeService.delete(typeId, user_id=user_id)
        except ExpenseTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Expense Type not found"}, code=404)
