# from Flask_Mongodb_redis.src.app.Controller.Controllers import MerchantIds
# app.register_blueprint(MerchantIds)

from Flask_Mongodb_redis.src.app.api.api_route import app

if __name__ == "__main__":
    app.run(debug=True)


