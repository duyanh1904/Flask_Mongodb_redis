from src.app.helper.GeneratorCode import GeneratorCodes
from src.app.Model.model_cache import *
from src.app.Model.base_model import BaseModel
from src.app.Model.base_model import UpdateCode
from flask import Blueprint, request, make_response
from flask_restful import Resource

class GetMerchantId(Resource):
    def get(self, code):
        return BaseModel(code).getCode()

class CacheMerchantId(Resource):
    def get(self, _id):
        return KeyCache().key_cache(_id)

class AddMerchantId(Resource):
    def post(self):
        genCode = GeneratorCodes(9).generator()
        return BaseModel(genCode).addCode()

class UpdateMerchantId(Resource):
    def put(self, _id):
        data = request.get_json()
        UpdateCode(data['code'], _id).updateCode()
        return make_response(jsonify({"code": str(data['code'])}), 200)

class DeleteMerchantId(Resource):
    def delete(self, code):
        return BaseModel(code).deleteCode()





