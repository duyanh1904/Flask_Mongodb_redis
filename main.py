from src.app.helper.connect_cache import app
import pymongo
from src.app.Model.base_model import Base_model
from src.app.Controller.Controllers import MerchantIds
from flask_cors import CORS
import logging

app.register_blueprint(MerchantIds)
logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG

CORS(app, resources=r'/api/*')

if __name__ == "__main__":
    with app.app_context():
        table.create_index([("name", pymongo.ASCENDING), ("slug", pymongo.ASCENDING)], unique=True)
    app.run(debug=True)


