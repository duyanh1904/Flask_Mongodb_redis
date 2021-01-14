from flask_cors import CORS
import logging
from Flask_Mongodb_redis.src.app.api.api import *
from Flask_Mongodb_redis.src.app.helper.connect_cache import app

app.register_blueprint(MerchantIds)
logging.basicConfig(level=logging.INFO, filename="global.log")
logging.getLogger('flask_cors').level = logging.DEBUG

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(debug=True)
