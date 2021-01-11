from src.app.helper.connect_cache import CacheClient
from src.app.helper.key_config import KeyCacheRedis
from src.app.helper.connect_redis import has_key, set_string, get_string
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import jsonify


client = MongoClient("mongodb://127.0.0.1:27017")
db = client.DB
table = db.merchant_id_table

class KeyCache():

    def key_cache(self, id):
        key_code = KeyCacheRedis.KEY_CODE + str(id)
        # check key
        if has_key(key_code):
            value_code = get_string(key_code)
            print("co key: ", value_code)
        else:
            code_detail = table.find_one({'_id': ObjectId(id)})
            print("code_detail: ", code_detail)
            value_code = code_detail.get('code')
            print("value_code: ", value_code)
        set_string(key_code, value_code)

        cached = CacheClient().get_cache(key_code)
        if cached:
            print('cached: ', cached)
            return cached
        chi_tiet_code = table.find_one({'_id': ObjectId(id)})
        print("chi_tiet_code: ", chi_tiet_code)
        id_user = chi_tiet_code.get('_id')
        print(id_user)
        code_user = chi_tiet_code.get('code')
        print('code_user: ', code_user)
        data = {
            '_id': str(id_user),
            'code': code_user
        }
        CacheClient().set_cache(key_code, data, 20)
        return jsonify({ 'id': id, 'code': code_user})