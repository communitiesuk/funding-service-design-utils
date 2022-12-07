from babel.core import negotiate_locale
from flask import request
from fsd_utils import CommonConfig
from werkzeug.http import parse_accept_header


def get_lang():
    # get locale from cookie if set
    locale_from_cookie = request.cookies.get(CommonConfig.FSD_LANG_COOKIE_NAME)
    if locale_from_cookie:
        return locale_from_cookie

    # if no cookie, get locale from accept header
    # if found guess preference based on user accept header
    accept_language_key = next(
        (
            key
            for key in request.headers.keys()
            if key.lower() == "accept-language"
        ),
        None,
    )
    if accept_language_key:
        preferred = [
            accept_language.replace("-", "_")
            for accept_language in parse_accept_header(
                request.headers.get(accept_language_key)
            ).values()
        ]

        negotiated_locale = negotiate_locale(preferred, ["en", "cy"])
        if negotiated_locale:
            return negotiated_locale

    # default is to return english
    return "en"
