from src.app.model.base_model import BaseModel
from pymongo.errors import DuplicateKeyError
from marshmallow import Schema, fields, validate
from flask import jsonify
from src.app.helper.redis_cache import *


class ReqSchema(Schema):
    MID = fields.Str(required=True, validate=validate.Length(min=5))


class CodeModel(BaseModel):

    def __init__(self, _code, _merchantId):
        self.merchantId = _merchantId
        self.code = _code

    @staticmethod
    def get_code(merchant_id):
        key_code = KeyCacheRedis.KEY_CODE + str(merchant_id)
        if has_key(key_code) is True:
            data = r.get(key_code)
            return data
        else:
            data = BaseModel.table.find_one({'merchantId': merchant_id})
            return data['code']

    def add_code(self):
        try:
            key_code = KeyCacheRedis.KEY_CODE + str(self.merchantId)
            set_string(key_code, self.code)
            BaseModel.table.insert_one({'code': self.code, 'merchantId': self.merchantId})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return self.code

    def update_code(self):
        key_code = KeyCacheRedis.KEY_CODE + str(self.merchantId)
        if has_key(key_code) is True:
            r.delete(key_code)
        try:
            BaseModel.table.update({"merchantId": self.merchantId}, {'$set': {"code": self.code}})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return self.code

    @staticmethod
    def delete_code(merchant_id):
        key_code = KeyCacheRedis.KEY_CODE + str(merchant_id)
        if has_key(key_code) is True:
            r.delete(key_code)
        try:
            BaseModel.table.remove({'merchantId': merchant_id})
        except TimeoutError:
            return jsonify(" Timeout Error "), 408
        return 'delete success'
