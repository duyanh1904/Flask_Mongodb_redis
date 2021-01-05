import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, url_for, jsonify, abort, request, jsonify
from pymongo import MongoClient
import string
import random


app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mydb
table = db.mytable



@app.route('/')
def home():
    code_list = table.find().sort("_id",pymongo.DESCENDING)
    return render_template("base.html", code_list=code_list)

@app.route("/add", methods = ['POST'])
def add():
    def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    table.insert({"code": id_generator()})
    return redirect('/')

@app.route("/delete")
def delete():
    key = request.values.get("_id")
    table.remove({"_id": ObjectId(key)})
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)