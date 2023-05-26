from unittest.mock import Mock

from fsd_utils.healthchecks.checkers import DbChecker
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.checkers import RedisChecker
from redis.exceptions import ConnectionError
from sqlalchemy.exc import ArgumentError


class TestCheckers:
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
        mock_db.session.execute.return_value = True
        db_checker = DbChecker(mock_db)

        result = db_checker.check()
        assert result[0] is True, "Unexpected check result"
        assert result[1] == "OK", "Unexpected check message"
        assert mock_db.session.execute.call_args.args[0].text == "SELECT 1"

    def testDbCheck_fail(self, flask_test_client):
        mock_db = Mock()
        mock_db.session.execute.side_effect = ArgumentError
        db_checker = DbChecker(mock_db)

        result = db_checker.check()
        assert result[0] is False, "Unexpected check result"
        assert result[1] == "Fail", "Unexpected check message"
        assert mock_db.session.execute.call_args.args[0].text == "SELECT 1"

    def testRedis_pass(self, flask_test_client):
        mock_redis = Mock()
        mock_redis.client_list.return_value = []
        redis_checker = RedisChecker(mock_redis)
        result = redis_checker.check()
        assert result[0] is True, "Unexpected result"
        assert result[1] == "OK", "Unexpected message"
        mock_redis.client_list.assert_called_once()

    def testRedis_fail(self, flask_test_client):
        mock_redis = Mock()
        mock_redis.client_list.side_effect = ConnectionError
        redis_checker = RedisChecker(mock_redis)
        result = redis_checker.check()
        assert result[0] is False, "Unexpected result"
        assert result[1] == "Fail", "Unexpected message"
        mock_redis.client_list.assert_called_once()
