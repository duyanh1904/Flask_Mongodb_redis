from Flask_Mongodb_redis.src.app.Model.base_model import BaseModel
from pymongo.errors import DuplicateKeyError
from marshmallow import Schema, fields, validate
from flask import jsonify
from Flask_Mongodb_redis.src.app.helper.key_config import KeyCacheRedis
# from Flask_Mongodb_redis.src.app.helper.connect_redis import has_key, get_string, set_string
from Flask_Mongodb_redis.src.app.helper.connect_cache import CacheClient


class ReqSchema(Schema):
    MID = fields.Str(required=True, validate=validate.Length(min=5))


class CodeModel(BaseModel):

    def __init__(self, _code, _merchant_id):
        self.merchantId = _merchant_id
        self.code = _code

    @staticmethod
    def get_code(merchant_id):
        key_code = KeyCacheRedis.KEY_CODE + str(merchant_id)
        cached = CacheClient().get_cache(key_code)
        if cached:
            print('cached: ', cached)
            return cached
        code_detail = BaseModel.table.find_one({'merchantId': str(merchant_id)})
        code_user = code_detail.get('code')
        data = {
            'code': code_user,
            'merchant_id': merchant_id
        }
        print("data: ", data)
        CacheClient().set_cache(key_code, data, 60)
        return jsonify(data)

    def add_code(self):
        try:
            BaseModel.table.insert_one({'code': self.code, 'merchantId': self.merchantId})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return jsonify({"code": self.code, "merchantId": self.merchantId})

    def update_code(self):
        try:
            BaseModel.table.update({"merchantId": self.merchantId}, {'$set': {"code": self.code}})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        key_code = KeyCacheRedis.KEY_CODE + str(self.merchantId)

        cached = CacheClient().get_cache(key_code)
        if cached:
            CacheClient.delete_cache(key_code)
        else:
            print('ko co key cache')
        return jsonify({'code': str(self.code)})

    @staticmethod
    def delete_code(self):
        try:
            BaseModel.table.remove({'merchantId': self.merchantId})
        except TimeoutError:
            return jsonify(" Timeout Error "), 408
        key_code = KeyCacheRedis.KEY_CODE + str(self.merchantId)
        print("key_code: ", key_code)
        # get key in cache dang exist
        cached = CacheClient().get_cache(key_code)
        print('cached: ', cached)
        # delete key cache
        if cached:
            CacheClient().delete_cache(key_code)
        else:
            print('ko ton tai cache!')
        return 'delete success'


