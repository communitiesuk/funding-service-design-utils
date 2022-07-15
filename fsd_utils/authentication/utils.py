import jwt as jwt
from flask import current_app

from .config import config_var_rs256_public_key


def _validate_token(token, key, algorithms):
    return jwt.decode(token, key, algorithms=algorithms)


def validate_token_rs256(token):
    key = current_app.config.get(config_var_rs256_public_key)
    return _validate_token(token, key, algorithms=["RS256"])
