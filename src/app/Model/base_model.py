from pymongo import MongoClient


class Base_model():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.DB
    table = db.merchant_id_table
