from functools import wraps

from flask import abort
from flask import current_app
from flask import g
from flask import redirect
from flask import request
from fsd_utils.authentication.utils import validate_token_rs256
from jwt import ExpiredSignatureError
from jwt import PyJWTError

from .config import config_var_auth_host
from .config import config_var_user_token_cookie_name
from .config import signout_route


def _failed_redirect():
    authenticator_host = current_app.config[config_var_auth_host]

    return abort(redirect(authenticator_host + signout_route))


def _check_access_token():
    user_token_cookie_name = current_app.config[
        config_var_user_token_cookie_name
    ]

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
        authenticator_host = current_app.config[config_var_auth_host]
        g.account_id = token_payload.get("accountId")
        g.is_authenticated = True
        g.logout_url = authenticator_host + signout_route
        return f(*args, **kwargs)

    return decorated
