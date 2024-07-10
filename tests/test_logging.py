import json

import pytest
from flask import Flask
from fsd_utils.logging import logging as fsd_logging
from fsd_utils.logging.logging import get_default_logging_config


@pytest.mark.parametrize(
    "fsd_log_level, expected_num_logs",
    (
        ("DEBUG", 6),  # 5 from test, +1 from `fsd_logging.init_app`
        ("INFO", 5),  # 4 from test, +1 from `fsd_logging.init_app`
        ("WARNING", 3),
        ("ERROR", 2),
        ("CRITICAL", 1),
    ),
)
def test_default_logging_respect_fsd_log_level(
    fsd_log_level, expected_num_logs, capsys
):
    """This test captures logging output on stdout to ensure that our standard logging config respects
    FSD_LOG_LEVEL correctly. But this means that the test will fail if pytest is called with the `-s` flag,
    which disables capturing.

    So hopefully if you're reading this because the test has failed, and you're using the `-s` flag, you can
    be reassured that's why it's failing.
    """
    app = Flask("test_app")
    app.config["FSD_LOG_LEVEL"] = fsd_log_level

    fsd_logging.init_app(app)

    with app.app_context():
        app.logger.debug("debug")
        app.logger.info("info")
        app.logger.warning("warning")
        app.logger.error("error")
        app.logger.critical("critical")

    assert len(capsys.readouterr().out.strip().splitlines()) == expected_num_logs


def test_default_logging_is_json(capsys):
    """This test captures logging output on stdout to ensure that our standard logging config respects
    FSD_LOG_LEVEL correctly. But this means that the test will fail if pytest is called with the `-s` flag,
    which disables capturing.

    So hopefully if you're reading this because the test has failed, and you're using the `-s` flag, you can
    be reassured that's why it's failing.
    """
    app = Flask("test_app")
    app.config["FSD_LOG_LEVEL"] = "DEBUG"

    fsd_logging.init_app(app)

    log_lines = capsys.readouterr().out.strip().splitlines()
    assert len(log_lines) == 1

    assert isinstance(json.loads(log_lines[0]), dict)


def test_logging_is_not_json_if_development_flask_env(capsys):
    """This test captures logging output on stdout to ensure that our standard logging config respects
    FSD_LOG_LEVEL correctly. But this means that the test will fail if pytest is called with the `-s` flag,
    which disables capturing.

    So hopefully if you're reading this because the test has failed, and you're using the `-s` flag, you can
    be reassured that's why it's failing.
    """
    app = Flask("test_app")
    app.config["FLASK_ENV"] = "development"
    app.config["FSD_LOG_LEVEL"] = "DEBUG"

    fsd_logging.init_app(app)

    log_lines = capsys.readouterr().out.strip().splitlines()
    assert len(log_lines) == 1

    with pytest.raises(ValueError):
        assert json.loads(log_lines[0])


def test_init_app_logging_can_take_custom_logging_config(capsys):
    """This test captures logging output on stdout to ensure that our standard logging config respects
    FSD_LOG_LEVEL correctly. But this means that the test will fail if pytest is called with the `-s` flag,
    which disables capturing.

    So hopefully if you're reading this because the test has failed, and you're using the `-s` flag, you can
    be reassured that's why it's failing.
    """
    app = Flask("test_app")
    app.config["FLASK_ENV"] = "development"
    app.config["FSD_LOG_LEVEL"] = "WARNING"

    log_config = get_default_logging_config(app)
    fsd_logging.init_app(app, log_config=log_config)

    with app.app_context():
        app.logger.warning("warning")
        app.logger.critical("critical")

    assert len(capsys.readouterr().out.strip().splitlines()) == 2

    log_config = get_default_logging_config(app)
    log_config["loggers"]["test_app"]["level"] = "CRITICAL"
    fsd_logging.init_app(app, log_config=log_config)

    with app.app_context():
        app.logger.warning("warning")
        app.logger.critical("critical")

    assert len(capsys.readouterr().out.strip().splitlines()) == 1
