import os

from flask import current_app


class Healthcheck(object):
    def __init__(self, app):
        self.flask_app = app
        self.flask_app.add_url_rule("/healthcheck", view_func=self.healthcheck_view, host="<host>")
        self.checkers = []

    def healthcheck_view(self, host=None):
        responseCode = 200
        response = {"checks": []}
        version = os.getenv("GITHUB_SHA")
        if version:
            response["version"] = version
        for checker in self.checkers:
            try:
                result = checker.check()
                current_app.logger.debug("Check %s returned %s", checker.name, result)
                response["checks"].append({checker.name: result[1]})
                if result[0] is False:
                    responseCode = 500
            except Exception:
                response["checks"].append({checker.name: "Failed - check logs"})
                current_app.logger.exception("Check %s failed with an exception", checker.name)
                responseCode = 500
        return response, responseCode

    def add_check(self, checker):
        self.checkers.append(checker)
