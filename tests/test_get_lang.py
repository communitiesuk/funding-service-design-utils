from fsd_utils.locale_selector.get_lang import get_lang


class TestGetLang:
    def test_get_lang_query_arg_valid(self, flask_test_client):
        with flask_test_client.application.test_request_context("/?lang=cy"):
            assert get_lang() == "cy"

    def test_get_lang_query_arg_invalid(self, flask_test_client):
        with flask_test_client.application.test_request_context("/?lang=fr"):
            assert get_lang() == "en"

    def test_get_lang_cookie_preference(self, flask_test_client):
        with flask_test_client.application.test_request_context(
            "/", headers={"Cookie": "language=cy"}
        ):
            assert get_lang() == "cy"

    def test_get_lang_accept_language_preference_en(self, flask_test_client):
        with flask_test_client.application.test_request_context(
            "/",
            headers={"Accept-Language": "en,en-GB;q=0.9,cy;q=0.8,en-US;q=0.7"},
        ):
            assert get_lang() == "en"

    def test_get_lang_accept_language_preference_cy(self, flask_test_client):
        with flask_test_client.application.test_request_context(
            "/",
            headers={
                "Accept-Language": "cy,en;q=0.9,en-GB;q=0.8,en-US;q=0.7"
            },  # noqa: E501
        ):
            assert get_lang() == "cy"
