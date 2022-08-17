from unittest.mock import ANY
from unittest.mock import Mock

from fsd_utils.healthchecks.checkers import DbChecker
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from sqlalchemy.exc import ArgumentError


class TestHealthcheck:
    def testHealthChecksSetup(self):
        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)
        assert health.checkers == [], "Checks not initialised"

    def testWithNoChecks(self):
        mock_app = Mock()
        health = Healthcheck(mock_app)
        mock_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)

        expected_dict = {"checks": []}

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 200, "Unexpected status code"

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

    def testRunningCheck_pass(self, flask_test_client):
        result = FlaskRunningChecker().check()
        assert result[0] is True, "Unexpected check result"
        assert result[1] == "OK", "Unexpected check message"

    # Don't pass in flask_test_client, therefore no flask.current_app,
    # therefore this check returns false
    def testRunningCheck_fail(self):
        result = FlaskRunningChecker().check()
        assert result[0] is False, "Unexpected check result"
        assert result[1] == "Fail", "Unexpected check message"

    def testDbCheck_pass(self):
        mock_db = Mock()
        mock_db.session = Mock()
        mock_db.session.execute.return_value = True
        db_checker = DbChecker(mock_db)

        result = db_checker.check()
        assert result[0] is True, "Unexpected check result"
        assert result[1] == "OK", "Unexpected check message"
        mock_db.session.execute.assert_called_with("SELECT 1")

    def testDbCheck_fail(self, flask_test_client):
        mock_db = Mock()
        mock_db.session = Mock()
        mock_db.session.execute.side_effect = ArgumentError
        db_checker = DbChecker(mock_db)

        result = db_checker.check()
        assert result[0] is False, "Unexpected check result"
        assert result[1] == "Fail", "Unexpected check message"
        mock_db.session.execute.assert_called_with("SELECT 1")
