from flask import request
from flask_restx import Resource, Namespace
from flask_accepts import responds, accepts

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
    def get(self):
        return SavingTypeService.get_all()

    @accepts(schema=SavingTypeSchema, api=api)
    @responds(schema=SavingTypeReturnSchema, api=api)
    @api.response(201, "Saving types successfully created.")
    def post(self):
        new_saving_type = SavingTypeService.create(request.parsed_obj)
        return make_json_response(data=SavingTypeReturnSchema().dump(new_saving_type), code=201)


@api.route('/type/<int:typeId>')
class SavingTypeIdResource(Resource):
    @responds(schema=SavingTypeReturnSchema, api=api)
    @api.response(200, "Saving type successfully retrieved.")
    def get(self, typeId):
        try:
            return SavingTypeService.get_one(typeId)
        except SavingTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Saving Type not found"}, code=404)
    
    @accepts(schema=SavingTypeSchema, api=api)
    @responds(schema=SavingTypeReturnSchema, api=api)
    @api.response(200, "Saving type successfully edited.")
    def put(self, typeId):
        try:
            return SavingTypeService.update(typeId, request.parsed_obj)
        except SavingTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Saving Type not found"}, code=404)
    
    @responds(status_code=204, api=api)
    @api.response(204, "Saving type successfully deleted.")
    def delete(self, typeId):
        try:
            return SavingTypeService.delete(typeId)
        except SavingTypeNotFoundException:
            return make_json_response(data={"code": 404, "message": "Saving Type not found"}, code=404)


@api.route('/')
class SavingValueResource(Resource):
    @responds(schema=SavingValueReturnSchema(many=True), api=api)
    @api.response(200, "Saving values successfully retrieved.")
    def get(self):
        return SavingValueService.get_all()

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
        try:
            return SavingValueService.get_one(id)
        except SavingValueNotFoundException:
           return make_json_response(data={"code": 404, "message": "Saving Value not found"}, code=404)

    @accepts(schema=SavingValueUpdateSchema, api=api)
    @responds(schema=SavingValueReturnSchema, api=api)
    @api.response(200, "Saving value successfully edited.")
    def put(self, id):
        try:
            return SavingValueService.update(id, request.parsed_obj)
        except:
           return make_json_response(data={"code": 404, "message": "Saving Value not found"}, code=404)

    @responds(status_code=204, api=api)
    @api.response(204, "Saving value successfully deleted.")
    def delete(self, id):
        try:
            return SavingValueService.delete(id)
        except SavingValueNotFoundException:
           return make_json_response(data={"code": 404, "message": "Saving Value not found"}, code=404)


@api.route('/summary/<int:year>/<int:month>')
class SavingSummaryResource(Resource):
    @responds(schema=SavingsSummarySchema(many=True), api=api)
    @api.response(200, "Savings summary successfully retrieved.")
    def get(self, year, month):
        return SavingValueService.get_savings_summary_list(year=year, month=month)
