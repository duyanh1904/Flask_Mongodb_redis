from flask_restful import Api, reqparse
from Flask_Mongodb_redis.src.app.Controller.Controllers import GetMerchantId, AddMerchantId,\
    UpdateMerchantId, DeleteMerchantId, DetailCode
from Flask_Mongodb_redis.src.app.helper.connect_cache import app

api = Api(app)

api.add_resource(GetMerchantId, '/')
api.add_resource(AddMerchantId, '/add')
api.add_resource(UpdateMerchantId, '/update/<merchant_id>')
api.add_resource(DeleteMerchantId, '/delete/<merchant_id>')
api.add_resource(DetailCode, '/code/<merchant_id>')

