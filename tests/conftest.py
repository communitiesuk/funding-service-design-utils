"""
Contains test configuration.
"""
import pytest
from flask import Flask


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
        app_context.app.config.update(
            {"FSD_LANG_COOKIE_NAME": "language", "COOKIE_DOMAIN": None}
        )
        with app_context.app.test_client() as test_client:
            yield test_client
