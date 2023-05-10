from flask import current_app
from flask import make_response
from flask import redirect
from flask import request
from fsd_utils import CommonConfig


class LanguageSelector:
    def __init__(self, app):
        self.flask_app = app
        self.flask_app.add_url_rule(
            "/language/<locale>", view_func=self.select_language
        )

    @staticmethod
    def select_language(locale):
        def get_cookie_domain(cookie_domain):
            if not cookie_domain:
                return None
            else:
                return cookie_domain

        response = make_response(
            redirect(request.referrer or request.args.get("return_url") or "/", 302)
        )
        response.set_cookie(
            CommonConfig.FSD_LANG_COOKIE_NAME,
            locale,
            domain=get_cookie_domain(current_app.config["COOKIE_DOMAIN"]),
            max_age=86400 * 30,  # 30 days
        )

        return response
