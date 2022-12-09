"""
Contains test configuration.
"""
from pathlib import Path

import pytest
from flask import Flask
from flask import g
from fsd_utils.authentication.decorators import login_requested
from fsd_utils.authentication.decorators import login_required


def create_app():
    app = Flask("test")
    return app


@pytest.fixture(scope="function")
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """

    with create_app().app_context() as app_context:
        _test_public_key_path = (
            str(Path(__file__).parent) + "/keys/rsa256/public.pem"
        )
        with open(_test_public_key_path, mode="rb") as public_key_file:
            rsa256_public_key = public_key_file.read()

        app_context.app.config.update(
            {
                "FSD_LANG_COOKIE_NAME": "language",
                "COOKIE_DOMAIN": None,
                "FSD_USER_TOKEN_COOKIE_NAME": "fsd-user-token",
                "AUTHENTICATOR_HOST": "https://authenticator",
                "RSA256_PUBLIC_KEY": rsa256_public_key,
            }
        )
        app_context.app.add_url_rule(
            "/mock_login_required_route",
            "mock_login_required_route",
            mock_login_required_route,
        )
        app_context.app.add_url_rule(
            "/mock_login_requested_route",
            "mock_login_requested_route",
            mock_login_requested_route,
        )
        with app_context.app.test_client() as test_client:
            yield test_client


@login_required
def mock_login_required_route():
    expected_g_attributes = {
        "is_authenticated": g.is_authenticated,
        "logout_url": g.logout_url,
        "account_id": g.account_id,
        "user": vars(g.user),
    }
    return expected_g_attributes


@login_requested
def mock_login_requested_route():
    expected_g_attributes = {
        "is_authenticated": g.is_authenticated,
        "logout_url": g.logout_url,
        "account_id": g.account_id,
        "user": vars(g.user) if "user" in g else None,
    }
    return expected_g_attributes
