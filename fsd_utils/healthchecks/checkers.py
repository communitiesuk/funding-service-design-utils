from typing import Tuple

from flask import current_app


class CheckerInterface:
    def check(self) -> Tuple[bool, str]:
        pass


class FlaskRunningChecker(CheckerInterface):
    def __init__(self):
        self.name = "check_flask_running"

    def check(self):
        if current_app:
            return True, "OK"
        else:
            return False, "Fail"


class DbChecker(CheckerInterface):
    def __init__(self, db):
        self.db = db
        self.name = "check_db"

    def check(self):
        from sqlalchemy.exc import SQLAlchemyError
        from sqlalchemy import text

        try:
            self.db.session.execute(text("SELECT 1"))
            return True, "OK"
        except SQLAlchemyError:
            current_app.logger.exception("DB Check failed")
            return False, "Fail"


class RedisChecker(CheckerInterface):
    def __init__(self, redis_client):  # TypeHint: FlaskRedis
        self.name = "check_redis"
        self.redis_client = redis_client

    def check(self):

        try:
            self.redis_client.client_list()
            return True, "OK"
        except Exception:
            current_app.logger.exception("Redis Check failed")
            return False, "Fail"
