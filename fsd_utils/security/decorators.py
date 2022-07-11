from functools import wraps
from urllib.parse import quote_plus

from flask import abort
from flask import current_app
from flask import redirect
from flask import request
from fsd_utils.security.utils import validate_token_rs256
from jwt import ExpiredSignatureError
from jwt import PyJWTError


def _failed_redirect(message: str = "Link expired or invalid"):
    auth_host_key = "AUTHENTICATOR_HOST"
    authenticator_host = current_app.config.get(auth_host_key)

    if not authenticator_host:
        current_app.logger.critical(
            f"Failed Redirect: {auth_host_key} " "not set in environ"
        )
        abort(500)

    return abort(
        redirect(
            f"{authenticator_host}"
            "/magic-links/new?error="
            f"{quote_plus(message)}"
        )
    )


def _check_access_token():
    user_token_cookie_key = "FSD_USER_TOKEN_COOKIE_NAME"
    user_token_cookie_name = current_app.config.get(user_token_cookie_key)
    if not user_token_cookie_name:
        current_app.logger.critical(
            f"Failed Check Token: {user_token_cookie_key} "
            "not set in environ"
        )
        abort(500)

    login_cookie = request.cookies.get(user_token_cookie_name)
    if not login_cookie:
        _failed_redirect()

    try:
        return validate_token_rs256(login_cookie)
    except (PyJWTError, ExpiredSignatureError):
        _failed_redirect()


def login_required(f):
    """Execute function if request contains valid JWT
    and pass account_id to route."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token()
        kwargs["account_id"] = token_payload.get("accountId")
        return f(*args, **kwargs)

    return decorated
