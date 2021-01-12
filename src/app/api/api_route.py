from flask_restful import Api
from Flask_Mongodb_redis.src.app.Controller.Controllers import GetMerchantId, AddMerchantId,\
    UpdateMerchantId, DeleteMerchantId, DetailCode
from flask import Flask
from Flask_Mongodb_redis.src.app.helper.connect_cache import app
# app = Flask(__name__)
api = Api(app)

api.add_resource(GetMerchantId, '/')
api.add_resource(AddMerchantId, '/add')
api.add_resource(UpdateMerchantId, '/update/<_id>')
api.add_resource(DeleteMerchantId, '/delete/<_id>')
api.add_resource(DetailCode, '/code/<_id>')

