from functools import wraps
from typing import List
from urllib.parse import urlencode

from flask import abort
from flask import current_app
from flask import g
from flask import redirect
from flask import Request
from flask import request
from fsd_utils.authentication.utils import validate_token_rs256
from jwt import ExpiredSignatureError
from jwt import PyJWTError
from werkzeug.exceptions import HTTPException

from .config import config_var_auth_host
from .config import config_var_logout_url_override
from .config import config_var_user_token_cookie_name
from .config import signout_route
from .config import SupportedApp
from .config import user_route
from .models import User


def _failed_redirect(return_app: SupportedApp | None):
    logout_url = _build_logout_url(return_app)
    return abort(redirect(logout_url))


def _failed_roles_redirect(roles_required: List[str]):
    authenticator_host = current_app.config[config_var_auth_host]

    params = {"roles_required": "|".join(roles_required)}

    return abort(redirect(authenticator_host + user_route + f"?{urlencode(params)}"))


def _check_access_token(return_app: SupportedApp | None = None, auto_redirect=True):
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
    user_token_cookie_name = current_app.config[config_var_user_token_cookie_name]

    login_cookie = request.cookies.get(user_token_cookie_name)
    if not login_cookie:
        if auto_redirect:
            _failed_redirect(return_app)
        return False

    try:
        return validate_token_rs256(login_cookie)
    except (PyJWTError, ExpiredSignatureError):
        if auto_redirect:
            _failed_redirect(return_app)
        return False


def _build_return_path(request: Request):
    query_string = ("?" + request.query_string.decode()) if request.query_string else ""
    return request.path + query_string


def _build_logout_url(return_app: SupportedApp | None):
    if override := current_app.config.get(config_var_logout_url_override):
        return override

    authenticator_host = current_app.config[config_var_auth_host]
    if return_app:
        return (
            authenticator_host
            + signout_route
            + f"?{urlencode({'return_app': return_app.value, 'return_path': _build_return_path(request)})}"
        )
    else:
        return authenticator_host + signout_route


def login_required(
    f=None, roles_required: List[str] = None, return_app: SupportedApp | None = None
):
    """
     Execute function if request contains valid JWT
     and pass account auth params to route as attributes
     on the flask request global 'g' object:
         - g.account_id: (str) users account id
         - g.is_authenticated: (bool) authentication status
         - g.user - this holds a User object and associated attributes
         - g.logout_url: (str) the service sign-out url
     If no valid auth JWT found then redirect to
     service config invalid login route
    :param f:
    :param return_app: app to return to after login
    :param roles_required: (List(str), optional) a list of the
            roles required to access the decorated route
    :return:
    """
    if f is None:
        return lambda f: login_required(
            f=f, roles_required=roles_required, return_app=return_app
        )

    @wraps(f)
    def _wrapper(*args, **kwargs):
        try:
            token_payload = _check_access_token(return_app=return_app)
            g.account_id = token_payload.get("accountId")
            g.user = User.set_with_token(token_payload)
        except HTTPException as e:
            if current_app.config.get(
                "FLASK_ENV"
            ) == "development" and current_app.config.get("DEBUG_USER_ON"):
                g.account_id = current_app.config.get("DEBUG_USER_ACCOUNT_ID")
                g.user = User(**current_app.config.get("DEBUG_USER"))
            else:
                raise e

        g.logout_url = _build_logout_url(return_app)
        g.is_authenticated = True
        if roles_required:
            if not any(
                role_required in g.user.roles for role_required in roles_required
            ):
                _failed_roles_redirect(roles_required)
        return f(*args, **kwargs)

    return _wrapper


def login_requested(f):
    """
    If request contains valid JWT
    then pass account auth params to route as attributes
    on the flask request global 'g' object:
        - g.account_id: (str) users account id
        - g.is_authenticated: (bool) authentication status
        - g.user - this holds a User object and associated attributes
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
            g.user = User.set_with_token(token_payload)
            g.is_authenticated = True
        else:
            g.account_id = None
            g.is_authenticated = False
        return f(*args, **kwargs)

    return decorated
