from src.app.helper.GeneratorCode import GeneratorCodes
from src.app.Model.base_model import ReqSchema
from src.app.helper.connect_cache import *
from src.app.helper.connect_redis import *
from src.app.helper.key_config import *
from src.app.Model.base_model import CodeModel
from flask import Blueprint, request
from marshmallow import Schema, fields, ValidationError
from flask import request, jsonify
import json

MerchantIds = Blueprint('MerchantIds', __name__)

@MerchantIds.route('/api/get/<merchantId>', methods=['GET'])
def get(merchantId):
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return CodeModel(data['code'], merchantId).getCode()

@MerchantIds.route('/api/add', methods=['POST'])
def add():
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    genCode = GeneratorCodes(9).generator()
    return CodeModel(genCode, data['merchantId']).addCode()

@MerchantIds.route("/api/update/<merchantId>", methods=['PUT'])
def update(merchantId):
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return CodeModel(data['code'], merchantId).updateCode()

@MerchantIds.route("/api/delete/<merchantId>", methods=['DELETE'])
def delete(merchantId):
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return CodeModel(data['code'], merchantId).deleteCode()

@MerchantIds.route('/api/code/<string:code>', methods=['GET'])
def get_code_id(code):
    key_code = KeyCacheRedis.KEY_CODE + str(code)
    # check key
    if has_key(key_code):
        value_code = get_string(key_code)
        print("co key: ", value_code)
    else:
        code_detail = Model.table.find_one({'code': code})
        print("code_detail: ", code_detail)
        value_code = code_detail.get('code')
        print("value_code: ", value_code)
    set_string(key_code, value_code)

    cached = CacheClient().get_cache(key_code)
    print('cached: ', cached)
    if cached:
        print("cached====================:", cached)
        return cached
    chi_tiet_code = BaseModel.table.find_one({'code': code})
    print("chi_tiet_code: ", chi_tiet_code)
    id_user = chi_tiet_code.get('_id')
    print(id_user)
    code_user = chi_tiet_code.get('code')
    print('code_user: ', code_user)
    data = {
        '_id': str(id_user),
        'code': code_user
    }
    CacheClient().set_cache(key_code, data, 10)
    return data







