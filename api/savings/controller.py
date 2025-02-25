from flask import request
from flask_restx import Resource, Namespace
from flask_accepts import responds, accepts
from flask_login import login_required, current_user

from app import api
from ..utils import make_json_response

from .exceptions import (
    SavingTypeNotFoundException,
    SavingValueNotFoundException
)
from .service import (
    SavingTypeService,
    SavingValueService
)
from .schema import (
    SavingTypeReturnSchema,
    SavingTypeSchema,
    SavingValueReturnSchema,
    SavingValueCreateSchema,
    SavingsSummarySchema,
    SavingValueUpdateSchema,
)


api = Namespace("Savings", description="Access to your savings")


@api.route('/type')
class SavingTypeResource(Resource):
    @responds(schema=SavingTypeReturnSchema(many=True), api=api)
    @api.response(200, "Saving types successfully retrieved.")
    @login_required
    def get(self):
        user_id = current_user.id
        return SavingTypeService.get_all(user_id=user_id)

    @accepts(schema=SavingTypeSchema, api=api)
    @responds(schema=SavingTypeReturnSchema, api=api)
    @api.response(201, "Saving types successfully created.")
    @login_required
    def post(self):
        user_id = current_user.id
        data = request.parsed_obj
        data['user_id'] = user_id
        new_saving_type = SavingTypeService.create(data)
        return make_json_response(data=SavingTypeReturnSchema().dump(new_saving_type), code=201)


@api.route('/type/<int:typeId>')
class SavingTypeIdResource(Resource):
    @responds(schema=SavingTypeReturnSchema, api=api)
    @api.response(200, "Saving type successfully retrieved.")
    @login_required
    def get(self, typeId):
        user_id = current_user.id
        try:
            return SavingTypeService.get_one(typeId, user_id=user_id)
        except SavingTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Saving Type not found"}, code=404)
    
    @accepts(schema=SavingTypeSchema, api=api)
    @responds(schema=SavingTypeReturnSchema, api=api)
    @api.response(200, "Saving type successfully edited.")
    @login_required
    def put(self, typeId):
        user_id = current_user.id
        try:
            return SavingTypeService.update(typeId, request.parsed_obj, user_id=user_id)
        except SavingTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Saving Type not found"}, code=404)
    
    @responds(status_code=204, api=api)
    @api.response(204, "Saving type successfully deleted.")
    @login_required
    def delete(self, typeId):
        user_id = current_user.id
        try:
            return SavingTypeService.delete(typeId, user_id=user_id)
        except SavingTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Saving Type not found"}, code=404)


@api.route('/')
class SavingValueResource(Resource):
    @responds(schema=SavingValueReturnSchema(many=True), api=api)
    @api.response(200, "Saving values successfully retrieved.")
    def get(self):
        user_id = current_user.id
        return SavingValueService.get_all(user_id=user_id)

    @accepts(schema=SavingValueCreateSchema, api=api)
    @responds(schema=SavingValueReturnSchema, api=api)
    @api.response(201, "Saving value successfully created.")
    def post(self):
        new_saving_value = SavingValueService.create(request.parsed_obj)
        return make_json_response(data=SavingValueReturnSchema().dump(new_saving_value), code=201)


@api.route('/<int:id>')
class SavingValueIdResource(Resource):
    @responds(schema=SavingValueReturnSchema, api=api)
    @api.response(200, "Saving value successfully retrieved.")
    def get(self, id):
        user_id = current_user.id
        try:
            return SavingValueService.get_one(id, user_id=user_id)
        except SavingValueNotFoundException:
           return make_json_response(data={"code": 404, "message": "Saving Value not found"}, code=404)

    @accepts(schema=SavingValueUpdateSchema, api=api)
    @responds(schema=SavingValueReturnSchema, api=api)
    @api.response(200, "Saving value successfully edited.")
    def put(self, id):
        user_id = current_user.id
        try:
            return SavingValueService.update(id, request.parsed_obj, user_id=user_id)
        except:
           return make_json_response(data={"code": 404, "message": "Saving Value not found"}, code=404)

    @responds(status_code=204, api=api)
    @api.response(204, "Saving value successfully deleted.")
    def delete(self, id):
        user_id = current_user.id
        try:
            return SavingValueService.delete(id, user_id=user_id)
        except SavingValueNotFoundException:
           return make_json_response(data={"code": 404, "message": "Saving Value not found"}, code=404)


@api.route('/summary/<int:year>/<int:month>')
class SavingSummaryResource(Resource):
    @responds(schema=SavingsSummarySchema(many=True), api=api)
    @api.response(200, "Savings summary successfully retrieved.")
    def get(self, year, month):
        user_id = current_user.id
        return SavingValueService.get_savings_summary_list(year=year, month=month, user_id=user_id)
