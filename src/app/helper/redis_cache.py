from flask_caching import Cache
from flask import Flask


# key config
from redis import StrictRedis


class KeyCacheRedis:
    KEY_CODE = "key_code_"

#connect cache


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

# connect_redis


r = StrictRedis('localhost', 6379, charset='utf-8', decode_responses=True)

def set_string(m_key, m_val):
    return r.set(name=m_key, value=m_val)


def get_string(m_key):
    return r.get(m_key)


def has_key(key):
    if r.get(key) is not None:
        return True
    else:
        return False


def delete_keys(key_pattern):
    for key in r.keys(key_pattern):
        return r.delete(key)
