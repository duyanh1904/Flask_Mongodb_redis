from flask import Blueprint, request
from flask.json import jsonify
from marshmallow import ValidationError
from src.app.controller.controllers import *
from src.app.model.code_model import ReqSchema


MerchantIds = Blueprint('MerchantIds', __name__)


@MerchantIds.route("/api/delete/<merchant_id>", methods=['DELETE'])
def delete(merchant_id):
    data = request.get_json()
    try:
        validate_mid = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validate_mid)
    except ValidationError as e:
        return jsonify(str(e)), 422
    message = RouteController().delete_mid(merchant_id)
    return jsonify({'message': message}), 200


@MerchantIds.route('/api/get/<merchant_id>', methods=['GET'])
def get(merchant_id):
    data = request.get_json()
    try:
        validate_mid = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validate_mid)
    except ValidationError as e:
        return jsonify(str(e)), 422
    code = RouteController().get_mid(merchant_id)
    return jsonify({'code': code}), 200


@MerchantIds.route('/api/add', methods=['POST'])
def add():
    data = request.get_json()
    try:
        validate_mid = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validate_mid)
    except ValidationError as e:
        return jsonify(str(e)), 422
    data = RouteController().add_mid(data['merchantId'])
    return jsonify({"code": data}), 200


@MerchantIds.route("/api/update/<merchant_id>", methods=['PUT'])
def update(merchant_id):
    data = request.get_json()
    try:
        validate_mid = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validate_mid)
    except ValidationError as e:
        return jsonify(str(e)), 422
    data = RouteController().update_mid(data['code'], merchant_id)
    return jsonify({"code": data}), 200