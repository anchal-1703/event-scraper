import redis
import json
r = redis.Redis(host='localhost', port=6379)


# Save events to Redis under a persistent key
# Print all keys
print(r.keys("*"))

# Check if "persistent:*" keys exist
print(r.keys("persistent:*"))

# Check a sample key value
key = r.keys("persistent:*")
if key:
    print(r.get(key[0]))
else:
    print("No persistent:* keys found.")
