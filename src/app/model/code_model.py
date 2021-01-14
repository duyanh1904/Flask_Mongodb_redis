from src.app.model.base_model import BaseModel
from pymongo.errors import DuplicateKeyError
from marshmallow import Schema, fields, validate
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
            r.set(key_code, data['code'])
            return data['code']

    def add_code(self):
        try:
            BaseModel.table.insert_one({'code': self.code, 'merchantId': self.merchantId})
        except DuplicateKeyError:
            raise DuplicateKeyError
        return self.code

    def update_code(self):
        key_code = KeyCacheRedis.KEY_CODE + str(self.merchantId)
        if has_key(key_code) is True:
            r.delete(key_code)
        try:
            BaseModel.table.update({"merchantId": self.merchantId}, {'$set': {"code": self.code}})
        except DuplicateKeyError:
            raise DuplicateKeyError
        return self.code

    @staticmethod
    def delete_code(merchant_id):
        key_code = KeyCacheRedis.KEY_CODE + str(merchant_id)
        if has_key(key_code) is True:
            r.delete(key_code)
        try:
            BaseModel.table.remove({'merchantId': merchant_id})
        except TimeoutError:
            raise TimeoutError
        return True
