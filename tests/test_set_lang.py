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
