from functools import wraps

from flask import abort
from flask import current_app
from flask import redirect
from flask import request
from fsd_utils.security.utils import validate_token_rs256
from jwt import ExpiredSignatureError


def _failed_redirect():
    return redirect(
        abort(
            redirect(
                f"{current_app.config.get('AUTHENTICATOR_HOST')}"
                "/magic-links/new?error=Link+expired+or+invalid"
            )
        )
    )


def _check_access_token():
    login_cookie = request.cookies.get(
        current_app.config.get("FSD_USER_TOKEN_COOKIE_NAME")
    )
    if not login_cookie:
        _failed_redirect()
    try:
        return validate_token_rs256(login_cookie)
    except ExpiredSignatureError:
        return _failed_redirect()


def login_required(f):
    """Execute function if request contains valid JWT
    and pass account_id to route."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token()
        kwargs["account_id"] = token_payload.get("accountId")
        return f(*args, **kwargs)

    return decorated
