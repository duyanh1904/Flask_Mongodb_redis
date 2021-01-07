from src.app.helper.connect_cache import app
from src.app.Controller.Controllers import MerchantIds
from flask_cors import CORS

app.register_blueprint(MerchantIds)

CORS(app)

if __name__ == "__main__":
    app.run(debug=True)


