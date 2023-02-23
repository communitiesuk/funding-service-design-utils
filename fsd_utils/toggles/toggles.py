from flipper import FeatureFlagClient, RedisFeatureFlagStore
from flask_redis import FlaskRedis

redis_store = FlaskRedis()

# Add feature flagging using Redis store
store = RedisFeatureFlagStore(redis_store, base_key='feature')
client = FeatureFlagClient(store)

feature_configuration = {
    "FLAGGING": False,
    "COMMENTING": True,
    "REMINDERS": False
}

for feature, toggle in feature_configuration.items():
    client.create(feature)
    if toggle:
        client.enable(feature)

def say_hi():
    return "I have been imported/ installed correctly G!!!!!!!!!!!!!!!!!!!!!!"
