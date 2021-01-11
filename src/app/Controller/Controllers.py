from bson.objectid import ObjectId
from Flask_Mongodb_redis.src.app.Model.base_model import BaseModel
from Flask_Mongodb_redis.src.app.helper.connect_cache import *
from Flask_Mongodb_redis.src.app.helper.connect_redis import *
from Flask_Mongodb_redis.src.app.helper.key_config import *
from Flask_Mongodb_redis.src.app.Model.model_cache import KeyCache
import string
import random
from flask import Blueprint, Response, request
from bson.json_util import dumps

MerchantIds = Blueprint('MerchantIds', __name__)


@MerchantIds.route('/')
def get_merchantId():
    merchant_id = BaseModel.table.find()
    code = list(merchant_id)
    data = dumps(code)
    return Response(data, mimetype="application/json", status=200)


@MerchantIds.route('/add', methods=['POST'])
def add():
    def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    BaseModel.table.insert_one({"code": id_generator()})
    return 'add success', 200


@MerchantIds.route("/update/<_id>", methods=['PUT'])
def update(_id):
    # update vao db
    code = request.form['code']
    BaseModel.table.update({"_id": ObjectId(_id)}, {'$set': {"code": code}})
    # create key config
    key_code = KeyCacheRedis.KEY_CODE + str(_id)
    print("key_code: ", key_code)
    # get key in cache dang exist
    cached = CacheClient().get_cache(key_code)
    print('cached: ', cached)
    # delete key cache
    if cached:
        CacheClient().delete_cache(key_code)
    else:
        print('ko ton tai cache!')
    return 'update success', 200


@MerchantIds.route("/delete/<_id>", methods=['DELETE'])
def delete(_id):
    BaseModel.table.remove({"_id": ObjectId(_id)})
    return 'delete success', 200


@MerchantIds.route('/code/<string:_id>', methods=['GET'])
def get_code_id(_id):
    return KeyCache().key_cache(_id)
