# from Flask_Mongodb_redis.src.app.Model.base_model import Base_model
# from key_config import KeyCacheRedis
# from Flask_Mongodb_redis.src.app.helper.connect_redis import has_key, set_string, get_string
# from Flask_Mongodb_redis.src.app.helper.connect_cache import CacheClient
#
#
# class UserCode(Base_model):
#
#     def __init__(self):
#         pass
#
#     def get_code_id(self, code):
#         key_code = KeyCacheRedis.KEY_CODE + str(code)
#         # check key
#         if has_key(key_code):
#             value_code = get_string(key_code)
#             print("co key: ", value_code)
#         # neu ko co truy van db lay ra luu vao redis
#         else:
#             code_detail = self.table.find_one({'code': code})
#             print("code_detail: ", code_detail)
#             value_code = code_detail.get('code')
#             print("value_code: ", value_code)
#         set_string(key_code, value_code)
#
#         cached = CacheClient().get_cache(key_code)
#         print('cached: ', cached)
#         if cached:
#             print("cached====================:", cached)
#             return cached
#         chi_tiet_code = self.table.find_one({'code': code})
#         print("chi_tiet_code: ", chi_tiet_code)
#         id_user = chi_tiet_code.get('_id')
#         print(id_user)
#         code_user = chi_tiet_code.get('code')
#         print('code_user: ', code_user)
#         data = {
#             '_id': str(id_user),
#             'code': code_user
#         }
#         CacheClient().set_cache(key_code, data, 10)
#         return data
#
#
# # if __name__ == "__main__":
# #     app.run(debug=True)
#     # data = UserCode().get_code_id('9L2SNPQYZ')
