from pymongo import MongoClient


class Base_model():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.mydb
    table = db.mytable
