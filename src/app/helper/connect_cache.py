from flask_caching import Cache
from flask import Flask
# from Flask_Mongodb_redis.src.app.api.api_route import app

cache = Cache(config={
    'CACHE_TYPE': "redis",
    'CACHE_DEFAULT_TIMEOUT': 30,
    'CACHE_REDIS_HOST': "localhost",
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 0,
    'CACHE_KEY_PREFIX': "my_key_prefix_code_",
    'CACHE_REDIS_URL': "redis://localhost:6379/0"
})
app = Flask(__name__)
cache.init_app(app)


class CacheClient:

    @staticmethod
    def set_cache(key, value, timeout):
        with app.app_context():
            return cache.set(key, value, timeout)

    @staticmethod
    def get_cache(key):
        with app.app_context():
            return cache.get(key)

    @staticmethod
    def delete_cache(key):
        with app.app_context():
            return cache.delete(key)


