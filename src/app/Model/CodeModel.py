from src.app.Model.base_model import BaseModel
from src.app.Model.ModelCache import KeyCache
from src.app.helper.connect_cache import *
from src.app.helper.connect_redis import *
from src.app.helper.key_config import *
from pymongo.errors import DuplicateKeyError
from marshmallow import Schema, fields, validate
from flask import jsonify


class ReqSchema(Schema):
    MID = fields.Str(required=True,validate=validate.Length(min=5))


class CodeModel(BaseModel):

    def __init__(self, _code, _merchantId):
        self.merchantId = _merchantId
        self.code = _code

    def getCode(self):
        BaseModel.table.find_one({'merchantId': self.merchantId})
        return jsonify({'code': self.code}, {'merchantId':self.merchantId})

    def addCode(self):
        try:
            BaseModel.table.insert_one({'code': self.code, 'merchantId': self.merchantId})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return jsonify({"code": self.code, "merchantId": self.merchantId}), 200

    def updateCode(self):
        try:
            BaseModel.table.update({"merchantId": self.merchantId}, {'$set': {"code": self.code}})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
            # create key config
        key_code = KeyCache().create_key(self.merchantId)
        print("key_code: ", key_code)
        # get key in cache dang exist
        cached = CacheClient().get_cache(key_code)
        print('cached: ', cached)
        # delete key cache
        if cached:
            CacheClient().delete_cache(key_code)
        else:
            print('ko ton tai cache!')
        return jsonify({'code': str(self.code)}), 200

    def deleteCode(self):
        try:
            BaseModel.table.remove({'code': self.code})
        except TimeoutError:
            return jsonify(" Timeout Error "), 408
        return 'delete success'

    def CacheCode(self):
        key_code = KeyCache().create_key(self.merchantId)
        # check key
        KeyCache().code_redis(key_code, self.merchantId)
        data = KeyCache().code_cache(key_code, self.merchantId)
        CacheClient().set_cache(key_code, data, 10)
        return jsonify({"code": self.code, "merchantId": self.merchantId}), 200



# class validateMerchantId():
#     def __init__(self, _merchantId):
#         self.merchantId = _merchantId
#
#     def validate(self):
#         try:
#             data = ({'MID': str(self.merchantId)})
#             ReqSchema().load(data)
#         except ValidationError as e:
#             return jsonify(str(e)), 422

