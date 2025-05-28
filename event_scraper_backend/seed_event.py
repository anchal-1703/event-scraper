import redis
import json
r = redis.Redis(host='localhost', port=6379)
events = [
    {
        "title": "Vivid Sydney Light Festival",
        "date": "2025-06-01",
        "venue": "Circular Quay",
        "url": "https://example.com/vivid"
    },
    {
        "title": "Sydney Comedy Gala",
        "date": "2025-06-10",
        "venue": "Sydney Opera House",
        "url": "https://example.com/comedy"
    }
]
r.set("persistent:test_events", json.dumps(events))
