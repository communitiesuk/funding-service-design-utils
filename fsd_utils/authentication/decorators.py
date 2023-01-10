from functools import wraps
from typing import List

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
from .config import user_route
from .models import User


def _failed_redirect():
    authenticator_host = current_app.config[config_var_auth_host]

    return abort(redirect(authenticator_host + signout_route))


def _failed_roles_redirect(roles_required: List[str]):
    authenticator_host = current_app.config[config_var_auth_host]

    return abort(
        redirect(
            authenticator_host
            + user_route
            + "?roles_required="
            + "|".join(roles_required)
        )
    )


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


def login_required(f=None, roles_required: List[str] = None):
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
    :param roles_required: (List(str), optional) a list of the
            roles required to access the decorated route
    :return:
    """
    if f is None:
        return lambda f: login_required(f=f, roles_required=roles_required)

    @wraps(f)
    def _wrapper(*args, **kwargs):
        if (
            current_app.config.get("FLASK_ENV") == "development"
            and current_app.config.get("DEBUG_USER_ROLE")
            and current_app.config.get("DEBUG_USER")
        ):
            g.account_id = "dev-account-id"
            g.user = User(**current_app.config.get("DEBUG_USER"))
        else:
            token_payload = _check_access_token()
            g.account_id = token_payload.get("accountId")
            g.user = User.set_with_token(token_payload)

        authenticator_host = current_app.config[config_var_auth_host]
        g.logout_url = authenticator_host + signout_route
        g.is_authenticated = True
        if roles_required:
            if not all(
                role_required in g.user.roles
                for role_required in roles_required
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
