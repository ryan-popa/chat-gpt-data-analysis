import os
import redis 

def redis_store():
    redis_host = os.environ.get("REDIS_HOST")
    redis_password = os.environ.get("REDIS_PASSWORD", "")

    if not redis_host:
        raise Exception("REDIS_HOST env var not set")
    return redis.Redis(host=redis_host, port=6379,
                        password=redis_password)