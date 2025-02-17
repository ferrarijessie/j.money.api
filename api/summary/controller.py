from flask import request
from flask_restx import Resource, Namespace
from flask_accepts import responds

from app import api

from .schema import SummaryReturnSchema, SummaryListReturnSchema
from .service import SummaryService


api = Namespace("Summary", description="Access to your finances summaries")


@api.route('/<int:year>/<int:month>')
class SummaryResource(Resource):
    @responds(schema=SummaryReturnSchema, api=api)
    @api.response(200, "Summary successfully retrieved.")
    def get(self, year, month):
        return SummaryService.get_summary(year=year, month=month)
        

@api.route('/list/<int:year>/<int:month>')
class SummaryListResource(Resource):
    @responds(schema=SummaryListReturnSchema(many=True), api=api)
    @api.response(200, "Summary list successfully retrieved.")
    def get(self, year, month):
        return SummaryService.get_summary_list(year=year, month=month)
