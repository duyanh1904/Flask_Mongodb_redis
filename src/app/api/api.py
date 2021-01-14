from flask import Blueprint, request
from flask.json import jsonify
from marshmallow import ValidationError
from Flask_Mongodb_redis.src.app.Controller.Controllers import *
from Flask_Mongodb_redis.src.app.Model.CodeModel import ReqSchema

MerchantIds = Blueprint('MerchantIds', __name__)


@MerchantIds.route("/api/delete/<merchant_id>", methods=['DELETE'])
def delete(merchant_id):
    # data = request.get_json()
    try:
        validate_mid = ({'MID': str(merchant_id)})
        ReqSchema().load(validate_mid)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return RouteController().delete_merchantId(merchant_id)


@MerchantIds.route('/api/get/<merchant_id>', methods=['GET'])
def get(merchant_id):
    # data = request.get_json()
    try:
        validate_mid = ({'MID': str(merchant_id)})
        ReqSchema().load(validate_mid)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return RouteController().get_merchantId(merchant_id)


@MerchantIds.route('/api/add', methods=['POST'])
def add():
    data = request.get_json()
    try:
        validate_mid = ({'MID': str(data['merchantId'])})
        ReqSchema().load(validate_mid)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return RouteController().add_merchantID(data['merchantId'])


@MerchantIds.route("/api/update/<merchant_id>", methods=['PUT'])
def update(merchant_id):
    data = request.get_json()
    try:
        validate_mid = ({'MID': str(merchant_id)})
        ReqSchema().load(validate_mid)
    except ValidationError as e:
        return jsonify(str(e)), 422
    return RouteController().update_merchatnId(data['code'], merchant_id)

