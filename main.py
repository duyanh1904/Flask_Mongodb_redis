import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
import string
import random


app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mydb
table = db.mytable


@app.route('/')
def home():
    posts =[1,2,3,4,5,6,7,8,9]
    code_list = table.find().sort("_id",pymongo.DESCENDING).limit(4)
    return render_template("base.html", code_list=code_list, posts = posts)

@app.route("/add", methods = ['POST'])
def add():
    def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    table.insert_one({"code": id_generator()})
    return redirect('/')

@app.route("/update")
def updateRoute():
    id = request.values.get("_id")
    code_list = table.find({"_id": ObjectId(id)})
    return render_template('update.html', code_list=code_list)


@app.route("/action_update",methods=['post'])
def update():
    code = request.values.get("code")
    id = request.values.get("_id")
    table.update({"_id": ObjectId(id)}, {'$set': {"code": code}})
    return redirect(url_for("home"))

@app.route("/delete")
def delete():
    id = request.values.get("_id")
    table.remove({"_id": ObjectId(id)})
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)