from babel import negotiate_locale
from flask import current_app
from flask import request
from fsd_utils import CommonConfig


def get_lang():

    # get lang if lang query arg is set
    language_from_query_args = request.args.get("lang")
    if language_from_query_args:
        if language_from_query_args not in ["cy", "en"]:
            current_app.logger.warning(
                f"Invalid language code {language_from_query_args}. Supported codes are 'cy' and 'en'."
            )
            return "en"
        else:
            return language_from_query_args

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
