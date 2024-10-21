from unittest.mock import ANY
from unittest.mock import Mock

from fsd_utils.locale_selector.set_lang import LanguageSelector


def test_set_lang(flask_test_client):
    mock_app = Mock()
    set_lang = LanguageSelector(mock_app)
    mock_app.add_url_rule.assert_called_with("/language/<locale>", view_func=ANY)
    with flask_test_client.application.test_request_context():
        response = set_lang.select_language("cy")
        response_cookie = response.headers.get("Set-Cookie")
        assert response_cookie is not None, "No cookie set for language"
        assert response_cookie.split(";")[0] == ("language" + "=cy")
        assert (
            "Secure" in response_cookie
        ), "Secure attribute not set for language cookie"
        assert (
            "SameSite=Lax" in response_cookie
        ), "SameSite attribute not set to Lax for language cookie"
        assert (
            "HttpOnly" in response_cookie
        ), "HttpOnly attribute not set for language cookie"


def test_set_language_cookie_attributes(flask_test_client):
    mock_app = Mock()
    set_lang = LanguageSelector(mock_app)
    with flask_test_client.application.test_request_context():
        response = flask_test_client.response_class()
        set_lang.set_language_cookie("cy", response)
        response_cookie = response.headers.get("Set-Cookie")
        assert response_cookie is not None, "No cookie set for language"
        assert (
            "Secure" in response_cookie
        ), "Secure attribute not set for language cookie"
        assert (
            "SameSite=Lax" in response_cookie
        ), "SameSite attribute not set to Lax for language cookie"
        assert (
            "HttpOnly" in response_cookie
        ), "HttpOnly attribute not set for language cookie"
