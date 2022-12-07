from babel import negotiate_locale
from flask import request
from fsd_utils import CommonConfig


def get_lang():
    # get locale from cookie if set
    locale_from_cookie = request.cookies.get(CommonConfig.FSD_LANG_COOKIE_NAME)
    if locale_from_cookie:
        return locale_from_cookie

    # otherwise guess preference based on user accept header
    preferred = [
        accept_language.replace("-", "_")
        for accept_language in request.accept_languages.values()
    ]
    negotiated_locale = negotiate_locale(preferred, ["en", "cy"])
    if negotiated_locale:
        return negotiated_locale

    # default is to return english
    return "en"
