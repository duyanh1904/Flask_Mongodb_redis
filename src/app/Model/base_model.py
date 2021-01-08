from pymongo import MongoClient
import pymongo
from pymongo.errors import DuplicateKeyError


class Base_model():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.DB
    table = db.merchant_id_table
    unique_index = table.create_index([('code', pymongo.ASCENDING)], unique = True)



