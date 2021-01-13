from src.app.helper.GeneratorCode import GeneratorCodes
from src.app.Model.CodeModel import ReqSchema
from src.app.Model.CodeModel import CodeModel
from flask import Blueprint, request
from marshmallow import Schema, fields, ValidationError
from flask import request, jsonify


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

@MerchantIds.route('/api/cache/<merchantId>', methods=['GET'])
def get_cache(merchantId):
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return CodeModel(data['code'], merchantId).CacheCode()








