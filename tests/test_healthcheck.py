import os
from unittest import mock
from unittest.mock import ANY
from unittest.mock import Mock

from fsd_utils.healthchecks.healthcheck import Healthcheck


class TestHealthcheck:
    @mock.patch.dict(os.environ, clear=True)
    def testHealthChecksSetup(self):
        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)
        assert health.checkers == [], "Checks not initialised"

    @mock.patch.dict(os.environ, clear=True)
    def testWithNoChecks(self):
        mock_app = Mock()
        health = Healthcheck(mock_app)
        mock_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)

        expected_dict = {"checks": []}

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 200, "Unexpected status code"

    @mock.patch.dict(os.environ, clear=True)
    def testWithChecksPassing_mocks(self, flask_test_client):
        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)

        expected_dict = {"checks": [{"check_a": "ok"}, {"check_b": "ok"}]}

        check_a = Mock()
        check_a.check.return_value = True, "ok"
        check_a.name = "check_a"
        health.add_check(check_a)
        check_b = Mock()
        check_b.check.return_value = True, "ok"
        check_b.name = "check_b"
        health.add_check(check_b)

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 200, "Unexpected status code"

    @mock.patch.dict(os.environ, clear=True)
    def testWithChecksFailing_mocks(self, flask_test_client):

        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)

        expected_dict = {"checks": [{"check_a": "fail"}, {"check_b": "ok"}]}

        check_a = Mock()
        check_a.check.return_value = False, "fail"
        check_a.name = "check_a"
        health.add_check(check_a)
        check_b = Mock()
        check_b.check.return_value = True, "ok"
        check_b.name = "check_b"
        health.add_check(check_b)

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 500, "Unexpected status code"

    @mock.patch.dict(os.environ, clear=True)
    def testWithChecksException_mocks(self, flask_test_client):

        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)

        expected_dict = {
            "checks": [{"check_a": "fail"}, {"check_b": "Failed - check logs"}]
        }

        check_a = Mock()
        check_a.check.return_value = False, "fail"
        check_a.name = "check_a"
        health.add_check(check_a)
        check_b = Mock()
        check_b.check.side_effect = TypeError
        check_b.name = "check_b"
        health.add_check(check_b)

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 500, "Unexpected status code"

    @mock.patch.dict(os.environ, {"GITHUB_SHA": "test-version"})
    def testShowsVersion(self):
        test_app = Mock()
        health = Healthcheck(test_app)
        result = health.healthcheck_view()
        assert result[0]["version"] == "test-version"
