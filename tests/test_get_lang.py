import pytest
from fsd_utils.locale_selector.get_lang import get_lang


class TestGetLang:
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

    @pytest.mark.parametrize(
        "accept_language_header_key",
        [
            "Accept-Language",
            "accept-language",
            "ACCEPT-LANGUAGE",
            "Accept-language",
            "accept-Language",
            "ACCEPT-language",
            "Accept-LANGUAGE",
        ],
    )
    def test_get_lang_accept_language_preference_regardless_of_header_key_case(
        self, flask_test_client, accept_language_header_key
    ):
        with flask_test_client.application.test_request_context(
            "/",
            headers={
                accept_language_header_key: "cy,en;q=0.9,en-GB;q=0.8,en-US;q=0.7"  # noqa: E501
            },
        ):
            assert get_lang() == "cy"
