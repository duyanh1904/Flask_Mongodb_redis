from flask import Blueprint, request
from flask.json import jsonify
from marshmallow import ValidationError
from src.app.Controller.Controllers import *
from src.app.Model.CodeModel import ReqSchema


MerchantIds = Blueprint('MerchantIds', __name__)

# app.register_blueprint(MerchantIds)


@MerchantIds.route("/api/delete/<merchantId>", methods=['DELETE'])
def delete(merchantId):
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return routeController().deleteMID(data['code'], merchantId)

@MerchantIds.route('/api/get/<merchantId>', methods=['GET'])
def get(merchantId):
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return routeController().getMID(data['code'], merchantId)

@MerchantIds.route('/api/add', methods=['POST'])
def add():
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return routeController().addMID(data['merchantId'])

@MerchantIds.route("/api/update/<merchantId>", methods=['PUT'])
def update(merchantId):
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return routeController().updateMID(data['code'], merchantId)


@MerchantIds.route('/api/cache/<merchantId>', methods=['GET'])
def get_cache(merchantId):
    data = request.get_json()
    try:
        validateMID = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validateMID)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return routeController().cacheMID(data['code'], merchantId)











