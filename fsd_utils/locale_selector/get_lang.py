from flask import request
from fsd_utils import CommonConfig


def get_lang():
    # get locale from cookie if set
    locale_from_cookie = request.cookies.get(CommonConfig.FSD_LANG_COOKIE_NAME)
    if locale_from_cookie:
        return locale_from_cookie
    else:
        return "en"

    # TODO: Restore this when we have translated into welsh
    # otherwise guess preference based on user accept header
    # from babel import negotiate_locale
    # preferred = [
    #     accept_language.replace("-", "_")
    #     for accept_language in request.accept_languages.values()
    # ]
    # return negotiate_locale(preferred, ["en", "cy"])
