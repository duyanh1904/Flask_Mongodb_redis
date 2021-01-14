from src.app.Model.CodeModel import CodeModel
from src.app.helper.GeneratorCode import GeneratorCodes
from src.app.helper.Redis_cache import *
# from src.app.helper.Redis_cache import CacheCode


class routeController:

    def get_mid(self, merchant_id):
        return CodeModel.get_code(merchant_id)

    def add_mid(self, merchant_id):
        gen_code = GeneratorCodes(9).generator()    #create random code
        key_code = KeyCacheRedis.KEY_CODE + str(merchant_id) #create key
        set_string(key_code, gen_code)        # store key in redis
        return CodeModel(gen_code, merchant_id).add_code()

    def update_mid(self, code, merchant_id):
        return CodeModel(code, merchant_id).update_code()

    def delete_mid(self,merchant_id):
        return CodeModel.delete_code(merchant_id)
