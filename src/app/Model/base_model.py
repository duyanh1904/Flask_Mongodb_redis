from pymongo import MongoClient
import pymongo
from flask import jsonify
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from marshmallow import Schema, fields, ValidationError, validate
from flask import request, jsonify
import json
from pprint import pprint

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.DB
table = db.merchant_id_table


class ReqSchema(Schema):
    MID = fields.Str(required=True,validate=validate.Length(min=5))


class CodeModel():

    def __init__(self, _code, _merchantId):
        self.merchantId = _merchantId
        self.code = _code

    def getCode(self):
        table.find_one({'merchantId': self.merchantId})
        return jsonify({'code': self.code}, {'merchantId':self.merchantId})

    def addCode(self):
        try:
            table.insert_one({'code': self.code, 'merchantId': self.merchantId})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return jsonify({"code": self.code, "merchantId": self.merchantId}), 200

    def updateCode(self):
        try:
            table.update({"merchantId": self.merchantId}, {'$set': {"code": self.code}})
        except DuplicateKeyError:
            return jsonify("Duplicate code"), 405
        return jsonify({'code': str(self.code)}), 200

    def deleteCode(self):
        try:
            table.remove({'code': self.code})
        except TimeoutError:
            return jsonify(" Timeout Error "), 408
        return 'delete success'


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

