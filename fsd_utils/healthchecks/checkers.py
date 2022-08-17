from typing import Tuple
from flask import current_app

class CheckerInterface:
    def check(self) -> Tuple[bool, str]:
        pass

class FlaskRunningChecker(CheckerInterface):
    def __init__(self):
        self.name = "check_running"

    def check(self):
        if(current_app):
            return True, "OK"
        else:
            return False, "Fail"

class DbChecker(CheckerInterface):

    def __init__(self, db):
        self.db = db
        self.name = "check_db"

    def check(self):
        from sqlalchemy.exc import SQLAlchemyError
        try:
            self.db.session.execute("SELECT 1")
            return True, "OK"
        except SQLAlchemyError as e:
            current_app.logger.exception("DB Check failed")
            return False, "Fail"