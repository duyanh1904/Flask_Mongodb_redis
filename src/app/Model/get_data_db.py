from src.app.Model.base_model import BaseModel
from bson.objectid import ObjectId

class GetData(BaseModel):
    def __init__(self):
        pass

    def get_data(self, _id):
        code_detail = BaseModel.table.find_one({'_id': ObjectId(_id)})
        return code_detail.get('code')