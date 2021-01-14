from pymongo import MongoClient


class BaseModel:
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.mydb
    table = db.mytable
