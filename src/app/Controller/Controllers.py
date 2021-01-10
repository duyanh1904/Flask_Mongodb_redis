from src.app.helper.GeneratorCode import GeneratorCodes
from src.app.helper.connect_cache import *
from src.app.helper.connect_redis import *
from src.app.helper.key_config import *
from src.app.Model.base_model import BaseModel
from src.app.Model.base_model import UpdateCode
from flask import Blueprint, request

MerchantIds = Blueprint('MerchantIds', __name__)

@MerchantIds.route('/api/get/<code>')
def getCode(code):
    return BaseModel(code).getCode()

@MerchantIds.route('/api/add', methods=['POST'])
def add():
    genCode = GeneratorCodes(9).generator()
    return BaseModel(genCode).addCode()

@MerchantIds.route("/api/update/<_id>", methods=['PUT'])
def update(_id):
    code = request.form['code']
    return UpdateCode(code, _id).updateCode()

@MerchantIds.route("/delete/<code>", methods=['DELETE'])
def delete(code):
    return BaseModel(code).deleteCode()
#timeout-> catch exception

@MerchantIds.route('/api/code/<string:code>', methods=['GET'])
def get_code_id(code):
    key_code = KeyCacheRedis.KEY_CODE + str(code)
    # check key
    if has_key(key_code):
        value_code = get_string(key_code)
        print("co key: ", value_code)
    else:
        code_detail = BaseModel.table.find_one({'code': code})
        print("code_detail: ", code_detail)
        value_code = code_detail.get('code')
        print("value_code: ", value_code)
    set_string(key_code, value_code)

    cached = CacheClient().get_cache(key_code)
    print('cached: ', cached)
    if cached:
        print("cached====================:", cached)
        return cached
    chi_tiet_code = BaseModel.table.find_one({'code': code})
    print("chi_tiet_code: ", chi_tiet_code)
    id_user = chi_tiet_code.get('_id')
    print(id_user)
    code_user = chi_tiet_code.get('code')
    print('code_user: ', code_user)
    data = {
        '_id': str(id_user),
        'code': code_user
    }
    CacheClient().set_cache(key_code, data, 10)
    return data







