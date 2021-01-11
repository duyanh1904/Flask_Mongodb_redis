from flask_restful import Api
from src.app.Controller.Controllers import GetMerchantId, UpdateMerchantId, DeleteMerchantId, \
    CacheMerchantId, AddMerchantId
from src.app.helper.connect_cache import app

api = Api(app)

api.add_resource(GetMerchantId, '/api/getCode/<code>')
api.add_resource(AddMerchantId, '/api/add')
api.add_resource(UpdateMerchantId, '/api/update/<_id>')
api.add_resource(DeleteMerchantId, '/api/delete/<code>')
api.add_resource(CacheMerchantId, '/api/code/<_id>')


