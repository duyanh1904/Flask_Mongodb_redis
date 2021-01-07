from bson.objectid import ObjectId
from src.app.Model.connectMongo import *
from src.app.Model.connect_cache import *
from src.app.Model.connect_redis import *
from src.app.Model.key_config import *
import string
import random
from flask import Blueprint, Response, request
from bson.json_util import dumps

MerchantIds = Blueprint('MerchantIds', __name__)

@MerchantIds.route('/')
def get_merchantId():
    merchantId = table.find()
    code = list(merchantId)
    data = dumps(code)
    return Response(data, mimetype="application/json", status=200)

@MerchantIds.route('/add', methods=['POST'])
def add():
    def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    table.insert_one({"code": id_generator()})
    return 'add success', 200

@MerchantIds.route("/update/<_id>",methods=['PUT'])
def update(_id):
    id = _id
    code = request.form['code']
    table.update({"_id": ObjectId(id)}, {'$set': {"code": code}})
    return 'update success', 200

@MerchantIds.route("/delete/<_id>",methods=['DELETE'])
def delete(_id):
    id = _id
    table.remove({"_id": ObjectId(id)})
    return 'delete success', 200

@MerchantIds.route('/code/<string:code>', methods=['GET'])
def get_code_id(code):
    key_code = KeyCacheRedis.KEY_CODE + str(code)
    # check key
    if has_key(key_code):
        value_code = get_string(key_code)
        print("co key: ", value_code)
    else:
        code_detail = table.find_one({'code': code})
        print("code_detail: ", code_detail)
        value_code = code_detail.get('code')
        print("value_code: ", value_code)
    set_string(key_code, value_code)

    cached = CacheClient().get_cache(key_code)
    print('cached: ', cached)
    if cached:
        print("cached====================:", cached)
        return cached
    chi_tiet_code = table.find_one({'code': code})
    print("chi_tiet_code: ", chi_tiet_code)
    id_user = chi_tiet_code.get('_id')
    print(id_user)
    code_user = chi_tiet_code.get('code')
    print('code_user: ', code_user)
    data = {
        '_id': str(id_user),
        'code': code_user
    }
    CacheClient().set_cache(key_code, data)
    return data