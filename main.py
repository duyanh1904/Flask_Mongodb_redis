import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, url_for, jsonify, abort, request, jsonify
from pymongo import MongoClient
import string
import random


app = Flask(__name__)

app.config['SECRET_KEY']='LongAndRandomSecretKey'
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mydb
table = db.mytable

def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/')
def home():
    code_list = table.find().sort("_id",pymongo.DESCENDING)
    return render_template("base.html", code_list=code_list,code = id_generator())

@app.route("/add", methods = ['POST'])
def add():
    # code = request.values.get(id_generator())
    table.insert({"code": id_generator()})
    return redirect('/')

@app.route("/delete")
def delete():
    key = request.values.get("_id")
    table.remove({"_id": ObjectId(key)})
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)