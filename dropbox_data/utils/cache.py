import redis
from functools import wraps
import json
import pickle
import logging

redis_client = redis.Redis(host='localhost', port=6379, db=0)
logger = logging.getLogger(__name__)

def cache_result(expire_time=86400):  # 24 horas
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                cached_result = redis_client.get(cache_key)
                
                if cached_result:
                    return pickle.loads(cached_result)
                    
                result = func(*args, **kwargs)
                redis_client.set(cache_key, pickle.dumps(result))
                return result
                
            except redis.exceptions.ConnectionError:
                # If Redis is unavailable, just execute the function without caching
                logger.warning("Redis unavailable - executing without cache")
                return func(*args, **kwargs)
        return wrapper
    return decorator