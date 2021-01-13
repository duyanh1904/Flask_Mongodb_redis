from src.app.Model.base_model import BaseModel
from src.app.helper.connect_cache import *
from src.app.helper.connect_redis import *
from src.app.helper.key_config import *
from pymongo.errors import DuplicateKeyError
from marshmallow import Schema, fields, validate
from flask import jsonify


class ReqSchema(Schema):
    MID = fields.Str(required=True,validate=validate.Length(min=5))


class CodeModel(BaseModel):

    def __init__(self, _code, _merchantId):
        self.merchantId = _merchantId
        self.code = _code

    def get_code(self):
        data = BaseModel.table.find_one({'merchantId': self.merchantId})
        key_code = KeyCache().create_key(self.merchantId)
        # check key
        KeyCache().code_redis(key_code, self.merchantId)
        data_cache = KeyCache().code_cache(key_code, self.merchantId)
        CacheClient().set_cache(key_code, data_cache, 10)
        return jsonify({'code': data['code'], 'merchantId': data['merchantId']})

    def add_code(self):
        try:
            BaseModel.table.insert_one({'code': self.code, 'merchantId': self.merchantId})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
            # create key config
        key_code = KeyCache().create_key(self.merchantId)
        print("key_code: ", key_code)
        # get key in cache dang exist
        cached = CacheClient().get_cache(key_code)
        print('cached: ', cached)
        # delete key cache
        if cached:
            CacheClient().delete_cache(key_code)
        else:
            print('ko ton tai cache!')
        return jsonify({"code": self.code, "merchantId": self.merchantId}), 200

    def update_code(self):
        try:
            BaseModel.table.update({"merchantId": self.merchantId}, {'$set': {"code": self.code}})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
            # create key config
        key_code = KeyCache().create_key(self.merchantId)
        print("key_code: ", key_code)
        # get key in cache dang exist
        cached = CacheClient().get_cache(key_code)
        print('cached: ', cached)
        # delete key cache
        if cached:
            CacheClient().delete_cache(key_code)
        else:
            print('ko ton tai cache!')
        return jsonify({'code': str(self.code)}), 200

    def delete_code(self):
        try:
            BaseModel.table.remove({'code': self.code})
        except TimeoutError:
            return jsonify(" Timeout Error "), 408
        # create key config
        key_code = KeyCache().create_key(self.merchantId)
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

    def cache_code(self):
        key_code = KeyCache().create_key(self.merchantId)
        # check key
        KeyCache().code_redis(key_code, self.merchantId)
        data = KeyCache().code_cache(key_code, self.merchantId)
        CacheClient().set_cache(key_code, data, 10)
        return jsonify({"code": self.code, "merchantId": self.merchantId}), 200


class KeyCache(BaseModel):
    def __init__(self):
        pass

    def create_key(self, _merchant_id):
        key_code = KeyCacheRedis.KEY_CODE + str(_merchant_id)
        return key_code

    def code_redis(self, key_code, _merchant_id):
        if has_key(key_code):
            value_code = get_string(key_code)
            print("co key: ", value_code)
        else:
            code_detail = BaseModel.table.find_one({'merchantId': _merchant_id})
            value_code = code_detail['code']
        return set_string(key_code, value_code)

    def code_cache(self, key_code, _merchant_id):
        cached = CacheClient().get_cache(key_code)
        if cached:
            print('cached: ', cached)
            return cached
        code_detail = BaseModel.table.find_one({'merchantId': _merchant_id})
        code_user = code_detail['code']
        data = {
            'code': code_user,
            'merchant_id': _merchant_id
        }
        CacheClient().set_cache(key_code, data, 60)
        return jsonify({'code': data['code'], 'merchant_id': data['merchant_id']})