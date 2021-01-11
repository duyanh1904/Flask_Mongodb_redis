from pymongo import MongoClient
import pymongo
from flask import jsonify
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from src.app.helper.connect_cache import CacheClient
from src.app.helper.key_config import KeyCacheRedis

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.DB
table = db.merchant_id_table
table.create_index([('code', pymongo.ASCENDING)],unique=True)


class BaseModel():

    def __init__(self, _merchantId):
        self.merchantId = _merchantId

    def getCode(self):
        table.find_one({'code': self.merchantId})
        return jsonify({'code': self.merchantId})

    def addCode(self):
        try:
            table.insert_one({'code': self.merchantId})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return jsonify({"code": self.merchantId}), 200

    def deleteCode(self):
        try:
            table.remove({'code': self.merchantId})
        except TimeoutError:
            return jsonify(" Timeout Error "), 408
        return 'delete success'

class UpdateCode():

    def __init__(self, _merchantId, _id):
        self.merchantId = _merchantId
        self.id = _id

    def updateCode(self):
        try:
            table.update({"_id": ObjectId(self.id)}, {'$set': {"code": self.merchantId}})
            # create key config
            key_code = KeyCacheRedis.KEY_CODE + str(self.id)
            print("key_code: ", key_code)
            # get key in cache dang exist
            cached = CacheClient().get_cache(key_code)
            print('cached: ', cached)
            # delete key cache
            if cached:
                CacheClient().delete_cache(key_code)
            else:
                print('Cache not available!')
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return jsonify({'code': str(self.merchantId)}), 200