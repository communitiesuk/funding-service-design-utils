from flask import Flask
from flask_redis import FlaskRedis
from flipper import FeatureFlagClient
from flipper import RedisFeatureFlagStore

redis_store = FlaskRedis(config_prefix="TOGGLES")


def initialise_toggles_redis_store(flask_app: Flask):
    redis_store.init_app(flask_app)


def create_toggles_client():
    store = RedisFeatureFlagStore(redis_store, base_key="feature")
    client = FeatureFlagClient(store)
    return client


def load_toggles(feature_configuration: dict, client: FeatureFlagClient):
    for feature, toggle in feature_configuration.items():
        client.create(feature)
        if toggle:
            client.enable(feature)
