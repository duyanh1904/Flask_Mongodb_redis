from src.app.helper.connect_cache import app
from src.app.Controller.Controllers import MerchantIds

app.register_blueprint(MerchantIds)

if __name__ == "__main__":
    app.run(debug=True)


