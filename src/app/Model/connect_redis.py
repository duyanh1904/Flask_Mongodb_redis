import redis

r = redis.Redis(host='localhost', port=6379, db=0)


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
        # print(key)
