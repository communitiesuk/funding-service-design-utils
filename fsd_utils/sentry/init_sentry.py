from os import getenv

import sentry_sdk
from fsd_utils import CommonConfig
from sentry_sdk.integrations.flask import FlaskIntegration


def init_sentry():
    if getenv("SENTRY_DSN"):
        sentry_sdk.init(
            environment=CommonConfig.FLASK_ENV,
            integrations=[
                FlaskIntegration(),
            ],
            traces_sample_rate=0.1,
        )
