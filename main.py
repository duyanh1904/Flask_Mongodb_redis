import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
import string
import random
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mydb
table = db.mytable

@app.route('/')
def home():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = int(request.args.get('page', 1))
    per_page = 4
    offset = (page - 1) * per_page
    code_list = table.find().sort("_id",pymongo.DESCENDING)
    files_for_render = code_list.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=code_list.count(), record_name = code_list, search = search,
                            css_framework='bootstrap3', per_page = 4, offset = offset)
    return render_template("base.html", code_list=files_for_render, pagination = pagination)

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