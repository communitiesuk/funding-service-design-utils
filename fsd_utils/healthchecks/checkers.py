from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

class CheckerInterface:
    def check(self):
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
        try:
            self.db.session.execute("SELECT 1")
            return True, "OK"
        except SQLAlchemyError as e:
            current_app.logger.exception("DB Check failed")
            return False, "Fail"