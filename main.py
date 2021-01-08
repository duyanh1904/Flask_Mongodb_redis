from src.app.helper.connect_cache import app
from src.app.Controller.Controllers import MerchantIds
from flask_cors import CORS
import logging

app.register_blueprint(MerchantIds)
logging.basicConfig(level=logging.INFO, filename = "global.log")
logging.getLogger('flask_cors').level = logging.DEBUG


cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(debug=True)


