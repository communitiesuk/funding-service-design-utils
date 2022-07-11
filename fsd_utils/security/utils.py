import jwt as jwt
from flask import current_app


def _validate_token(token, key, algorithms):
    return jwt.decode(token, key, algorithms=algorithms)


def validate_token_rs256(token):
    key = current_app.config.get("RSA256_PUBLIC_KEY")
    return _validate_token(token, key, algorithms=["RS256"])
