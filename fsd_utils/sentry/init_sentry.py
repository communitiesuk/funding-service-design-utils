from os import getenv

import sentry_sdk
from fsd_utils import CommonConfig
from sentry_sdk.integrations.flask import FlaskIntegration


def _traces_sampler(sampling_context):
    wsgi_environ = sampling_context.get("wsgi_environ")
    if wsgi_environ and (
        wsgi_environ.get("PATH_INFO") == "/healthcheck"
        or wsgi_environ.get("HTTP_USER_AGENT" == "locust performance tests")
    ):
        # Drop this transaction, by setting its sample rate to 0%
        return 0
    else:
        # Default sample rate for all others (replaces traces_sample_rate)
        return float(getenv("SENTRY_TRACES_SAMPLE_RATE", "0.02"))


def init_sentry():
    if getenv("SENTRY_DSN"):
        sentry_sdk.init(
            environment=CommonConfig.FLASK_ENV,
            integrations=[
                FlaskIntegration(),
            ],
            traces_sampler=_traces_sampler,
            profiles_sampler=_traces_sampler,
            release=getenv("GITHUB_SHA"),
        )


def clear_sentry():
    if getenv("SENTRY_DSN"):
        sentry_sdk.set_user(None)
