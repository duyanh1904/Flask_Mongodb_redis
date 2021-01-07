from flask import Flask
from flask import Blueprint
from flask_restful import Api
from src.app.Controller.route import *

app = Flask(__name__)

app.register_blueprint(MerchantIds)

if __name__ == "__main__":
    app.run(debug=True)


