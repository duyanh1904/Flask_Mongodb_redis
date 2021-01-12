from src.app.helper.connect_cache import CacheClient
from src.app.helper.key_config import KeyCacheRedis
from src.app.helper.connect_redis import has_key, set_string, get_string
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import jsonify
from src.app.Model.get_data_db import GetData



client = MongoClient("mongodb://127.0.0.1:27017")
db = client.DB
table = db.merchant_id_table

class KeyCache(BaseModel):
    def __init__(self):
        pass

    def create_key(self, _id):
        key_code = KeyCacheRedis.KEY_CODE + str(_id)
        return key_code

    def redis_conn(self, key_code, _id):
        if has_key(key_code):
            value_code = get_string(key_code)
            print("co key: ", value_code)
        else:
            value_code = GetData().get_data(_id)
        return set_string(key_code, value_code)

    def cache_conn(self, key_code, _id):
        cached = CacheClient().get_cache(key_code)
        if cached:
            print('cached: ', cached)
            return cached
        code_user = GetData().get_data(_id)
        data = {
            '_id': str(_id),
            'code': code_user
        }
        CacheClient().set_cache(key_code, data, 200)
        return data
