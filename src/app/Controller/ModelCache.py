from src.app.Model.base_model import BaseModel
from src.app.helper.connect_cache import CacheClient
from src.app.helper.key_config import KeyCacheRedis
from src.app.helper.connect_redis import *
from flask import jsonify


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
            value_code = code_detail.get('code')
        return set_string(key_code, value_code)

    def code_cache(self, key_code, _merchant_id):
        cached = CacheClient().get_cache(key_code)
        if cached:
            print('cached: ', cached)
            return cached
        code_detail = BaseModel.table.find_one({'merchant_id': _merchant_id})
        code_user = code_detail.get('code')
        data = {
            'code': code_user,
            'merchant_id': _merchant_id
        }
        CacheClient().set_cache(key_code, data, 60)
        return jsonify(data)