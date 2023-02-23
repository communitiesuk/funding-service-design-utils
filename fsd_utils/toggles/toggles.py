import redis
from flipper import FeatureFlagClient, RedisFeatureFlagStore
from flask_redis import FlaskRedis
from fsd_utils.healthchecks.checkers import RedisChecker

redis_store = FlaskRedis()


r = redis.Redis(host='localhost', port=6379, db=0)

# Add feature flagging using Redis store
store = RedisFeatureFlagStore(redis_store, base_key='feature')
features = FeatureFlagClient(store)

feature_configuration = {
    "FLAGGING": True,
    "COMMENTING": True,
    "REMINDERS": False
}

for feature, toggle in feature_configuration.items():
    features.create(feature)
    if toggle:
        features.enable(feature)
