from flask import Response, current_app, make_response, redirect, request

from fsd_utils import CommonConfig


class LanguageSelector:
    @staticmethod
    def get_cookie_domain(cookie_domain):
        if not cookie_domain:
            return None
        else:
            return cookie_domain

    @staticmethod
    def set_language_cookie(locale: str, response: Response):
        response.set_cookie(
            CommonConfig.FSD_LANG_COOKIE_NAME,
            locale,
            domain=LanguageSelector.get_cookie_domain(current_app.config["COOKIE_DOMAIN"]),
            max_age=86400 * 30,  # 30 days
        )

    def __init__(self, app):
        self.flask_app = app
        self.flask_app.add_url_rule("/language/<locale>", view_func=self.select_language)

    @staticmethod
    def select_language(locale):
        # TODO: Perform additional validation on referrer
        response = make_response(redirect(request.referrer or "/", 302))
        LanguageSelector.set_language_cookie(locale, response)

        return response
