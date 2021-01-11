from src.app.helper.GeneratorCode import GeneratorCodes
from src.app.Model.model_cache import *
from src.app.Model.base_model import BaseModel
from src.app.Model.base_model import UpdateCode
from flask import Blueprint, request


MerchantIds = Blueprint('MerchantIds', __name__)

@MerchantIds.route('/api/get/<code>')
def getCode(code):
    return BaseModel(code).getCode()

@MerchantIds.route('/api/add', methods=['POST'])
def add():
    genCode = GeneratorCodes(9).generator()
    return BaseModel(genCode).addCode()

@MerchantIds.route("/api/update/<_id>", methods=['PUT'])
def update(_id):
    data = request.get_json()
    return UpdateCode(data['code'], _id).updateCode()

@MerchantIds.route("/delete/<code>", methods=['DELETE'])
def delete(code):
    return BaseModel(code).deleteCode()

@MerchantIds.route('/code/<string:_id>', methods=['GET'])
def get_code_id(_id):
    return KeyCache().key_cache(_id)




