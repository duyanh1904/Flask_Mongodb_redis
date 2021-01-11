from bson.objectid import ObjectId
from Flask_Mongodb_redis.src.app.Model.base_model import BaseModel
from Flask_Mongodb_redis.src.app.helper.connect_cache import *
from Flask_Mongodb_redis.src.app.helper.key_config import *
from Flask_Mongodb_redis.src.app.Model.model_cache import KeyCache
import string
import random
from flask import Blueprint, Response, request
from bson.json_util import dumps
from flask_restful import Resource

MerchantIds = Blueprint('MerchantIds', __name__)


class GetMerchantId(Resource):
    # @MerchantIds.route('/')
    def get(self):
        merchant_id = BaseModel.table.find()
        code = list(merchant_id)
        data = dumps(code)
        return Response(data, mimetype="application/json", status=200)


class AddMerchantId(Resource):
    # @MerchantIds.route('/add', methods=['POST'])
    def post(self):
        def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

        BaseModel.table.insert_one({"code": id_generator()})
        return 'add success', 200


class UpdateMerchantId(Resource):
    # @MerchantIds.route("/update/<_id>", methods=['PUT'])
    def put(self, _id):
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


class DeleteMerchantId(Resource):
    # @MerchantIds.route("/delete/<_id>", methods=['DELETE'])
    def delete(self, _id):
        BaseModel.table.remove({"_id": ObjectId(_id)})
        return 'delete success', 200


class DetailCode(Resource):
    # @MerchantIds.route('/code/<string:_id>', methods=['GET'])
    def get(self, _id):
        return KeyCache().key_cache(_id)
