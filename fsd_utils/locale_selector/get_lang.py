from babel import negotiate_locale
from flask import current_app
from flask import request


def get_lang():
    # get locale from cookie if set
    locale_from_cookie = request.cookies.get(
        current_app.config["FSD_LANG_COOKIE_NAME"]
    )
    if locale_from_cookie:
        return locale_from_cookie
    # otherwise guess preference based on user accept header
    preferred = [
        accept_language.replace("-", "_")
        for accept_language in request.accept_languages.values()
    ]
    return negotiate_locale(preferred, ["en", "cy"])
