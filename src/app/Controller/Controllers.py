from Flask_Mongodb_redis.src.app.Model.CodeModel import KeyCache
from Flask_Mongodb_redis.src.app.Model.base_model import BaseModel
from Flask_Mongodb_redis.src.app.helper.connect_cache import CacheClient
from Flask_Mongodb_redis.src.app.helper.GeneratorCode import GeneratorCodes
from flask import jsonify
from pymongo.errors import DuplicateKeyError


class RouteController:

    def get_merchantId(self, merchant_id):
        key_merchant_id = KeyCache().create_key(merchant_id)
        KeyCache().code_redis(key_merchant_id, merchant_id)
        result = KeyCache().code_cache(key_merchant_id, merchant_id)
        return result

    def add_merchantID(self, merchant_id):
        genCode = GeneratorCodes(9).generator()
        try:
            BaseModel.table.insert_one({'code': genCode, 'merchantId': merchant_id})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return jsonify({"code": genCode, "merchantId": merchant_id}), 200

    def update_merchatnId(self, code, merchant_id):
        try:
            BaseModel.table.update({"merchantId": merchant_id}, {'$set': {"code": code}})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        # create key config
        key_code = KeyCache().create_key(merchant_id)
        print("key_code: ", key_code)
        # get key in cache dang exist
        cached = CacheClient().get_cache(key_code)
        print('cached: ', cached)
        # delete key cache
        if cached:
            CacheClient().delete_cache(key_code)
        else:
            print('ko ton tai cache!')
        return jsonify({'code': str(code)}), 200

    def delete_merchantId(self, merchant_id):
        try:
            BaseModel.table.remove({'merchantId': merchant_id})
        except TimeoutError:
            return jsonify(" Timeout Error "), 408
        key_code = KeyCache().create_key(merchant_id)
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

