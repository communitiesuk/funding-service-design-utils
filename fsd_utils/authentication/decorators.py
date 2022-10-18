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


def _check_access_token(auto_redirect=True):
    """
    Check the expected auth cookie for a
    valid JWT token.
    :param auto_redirect: (bool) redirect on failed authentication if True
    :return:
        - If a valid JWT token is found then return token claims
        - If no valid token is found:
            -- If auto_redirect is True then issue a _failed_redirect()
            -- If auto_redirect is False then return False
    """
    user_token_cookie_name = current_app.config[
        config_var_user_token_cookie_name
    ]

    login_cookie = request.cookies.get(user_token_cookie_name)
    if not login_cookie:
        if auto_redirect:
            _failed_redirect()
        return False

    try:
        return validate_token_rs256(login_cookie)
    except (PyJWTError, ExpiredSignatureError):
        if auto_redirect:
            _failed_redirect()
        return False


def login_required(f):
    """
    Execute function if request contains valid JWT
    and pass account auth params to route as attributes
    on the flask request global 'g' object:
        - g.account_id: (str) users account id
        - g.is_authenticated: (bool) authentication status
        - g.logout_url: (str) the service sign-out url
    If no valid auth JWT found then redirect to
    service config invalid login route
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token()
        authenticator_host = current_app.config[config_var_auth_host]
        g.account_id = token_payload.get("accountId")
        g.is_authenticated = True
        g.logout_url = authenticator_host + signout_route
        return f(*args, **kwargs)

    return decorated


def login_requested(f):
    """
    If request contains valid JWT
    then pass account auth params to route as attributes
    on the flask request global 'g' object:
        - g.account_id: (str) users account id
        - g.is_authenticated: (bool) authentication status
        - g.logout_url: (str) the service sign-out url
    If no valid auth JWT found then update the g.is_authenticated
    variable to False and the g.account_id to None
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token(auto_redirect=False)
        authenticator_host = current_app.config[config_var_auth_host]
        g.logout_url = authenticator_host + signout_route
        if token_payload and isinstance(token_payload, dict):
            g.account_id = token_payload.get("accountId")
            g.is_authenticated = True
        else:
            g.account_id = None
            g.is_authenticated = False
        return f(*args, **kwargs)

    return decorated
