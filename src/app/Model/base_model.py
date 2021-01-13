from pymongo import MongoClient

class BaseModel():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.DB
    table = db.merchant_id_table