import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

_redis_client = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)


def get_cache(key: str):
    value = _redis_client.get(key)
    if value is None:
        return None
    return json.loads(value)


def set_cache(key: str, value, expire_seconds: int = 60):
    _redis_client.set(key, json.dumps(value), ex=expire_seconds)


def delete_cache(key: str):
    _redis_client.delete(key)
