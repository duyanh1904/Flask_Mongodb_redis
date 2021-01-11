from flask_cors import CORS
from src.app.CallApi.CallApis import *

import logging


logging.basicConfig(level=logging.INFO, filename = "global.log")
logging.getLogger('flask_cors').level = logging.DEBUG


cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(debug=True)


