import redis
import json
from config import Config

r = redis.from_url(Config.REDIS_URL)

def get_cached_events(cache_key=None):
    key = cache_key or Config.EVENTS_KEY
    data = r.get(key)
    return json.loads(data) if data else None

def get_persistent_events(cache_key=None):
    # Get events from persistent storage (without expiry)
    key = f"persistent:{cache_key}" if cache_key else f"persistent:{Config.EVENTS_KEY}"
    data = r.get(key)
    return json.loads(data) if data else None

def cache_events(events, cache_key=None, persistent=False):
    key = cache_key or Config.EVENTS_KEY
    
    # Store in regular cache with expiry
    r.setex(key, Config.TTL_SECONDS, json.dumps(events))
    
    # If persistent flag is True or events exist, store in persistent storage without expiry
    if persistent or events:
        persistent_key = f"persistent:{key}"
        r.set(persistent_key, json.dumps(events))  # No expiry

def save_email(email):
    r.sadd(Config.EMAIL_LIST_KEY, email)