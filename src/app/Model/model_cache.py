from Flask_Mongodb_redis.src.app.helper.connect_cache import CacheClient
from Flask_Mongodb_redis.src.app.helper.key_config import KeyCacheRedis
from Flask_Mongodb_redis.src.app.Model.base_model import BaseModel
from Flask_Mongodb_redis.src.app.helper.connect_redis import has_key, set_string, get_string
from bson.objectid import ObjectId


class KeyCache(BaseModel):

    def __init__(self):
        pass

    def key_cache(self, id):
        key_code = KeyCacheRedis.KEY_CODE + str(id)
        # check key
        if has_key(key_code):
            value_code = get_string(key_code)
            print("co key: ", value_code)
        else:
            code_detail = BaseModel.table.find_one({'_id': ObjectId(id)})
            print("code_detail: ", code_detail)
            value_code = code_detail.get('code')
            print("value_code: ", value_code)
        set_string(key_code, value_code)

        cached = CacheClient().get_cache(key_code)
        if cached:
            print('cached: ', cached)
            return cached
        chi_tiet_code = BaseModel.table.find_one({'_id': ObjectId(id)})
        print("chi_tiet_code: ", chi_tiet_code)
        id_user = chi_tiet_code.get('_id')
        print(id_user)
        code_user = chi_tiet_code.get('code')
        print('code_user: ', code_user)
        data = {
            '_id': str(id_user),
            'code': code_user
        }
        CacheClient().set_cache(key_code, data, 200)
        return data
