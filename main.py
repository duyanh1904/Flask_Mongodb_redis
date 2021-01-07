from Flask_Mongodb_redis.src.app.helper.connect_cache import app
from Flask_Mongodb_redis.src.app.Controller.Controllers import MerchantIds

app.register_blueprint(MerchantIds)

if __name__ == "__main__":
    app.run(debug=True)


