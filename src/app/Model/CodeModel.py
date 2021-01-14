from src.app.Model.base_model import BaseModel
from pymongo.errors import DuplicateKeyError
from marshmallow import Schema, fields, validate
from flask import jsonify
from src.app.helper.Redis_cache import *

class ReqSchema(Schema):
    MID = fields.Str(required=True,validate=validate.Length(min=5))



class CodeModel(BaseModel):

    def __init__(self, _code, _merchantId):
        self.merchantId = _merchantId
        self.code = _code

    @staticmethod
    def get_code(merchant_id):
        key_code = KeyCacheRedis.KEY_CODE + str(merchant_id)
        if has_key(key_code) is True:
            data = r.get(key_code)
            return jsonify({'code': data})
        else:
            data = BaseModel.table.find_one({'merchantId': merchant_id})
            return jsonify({'code1': data['code']})


    def add_code(self):
        try:
            BaseModel.table.insert_one({'code': self.code, 'merchantId': self.merchantId})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return jsonify({"code": self.code, "merchantId": self.merchantId}), 200

    def update_code(self):
        key_code = KeyCacheRedis.KEY_CODE + str(self.merchantId)
        if has_key(key_code) is True:
            r.delete(key_code)
        else:
            try:
                BaseModel.table.update({"merchantId": self.merchantId}, {'$set': {"code": self.code}})
            except DuplicateKeyError:
                return jsonify("Duplicate code"), 405
        return jsonify({'code': str(self.code)}), 200


    def delete_code(self):
        key_code = KeyCacheRedis.KEY_CODE + str(self.merchantId)
        if has_key(key_code) is True:
            r.delete(key_code)
        else:
            try:
                BaseModel.table.remove({'code': self.code})
            except TimeoutError:
                return jsonify(" Timeout Error "), 408
        return 'delete success'


