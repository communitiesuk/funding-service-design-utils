import os
from unittest import mock

import pytest

from fsd_utils.config.commonconfig import CommonConfig


@pytest.mark.parametrize(
    "flask_env, env_secret_key, exp_secret_key",
    [
        ("dev", "dev_key", "dev_key"),
        ("development", "dev_key", "dev_key"),
        ("uat", "abc123", "abc123"),
        ("development", "", "dev-secret"),
        ("unit_test", "", "dev-secret"),
        ("prod", "prod_secret", "prod_secret"),
    ],
)
def test_config(flask_env, env_secret_key, exp_secret_key):
    with mock.patch.dict(os.environ, {"SECRET_KEY": env_secret_key}):
        result = CommonConfig._resolve_secret_key(flask_env)
    assert result == exp_secret_key


@pytest.mark.parametrize(
    "flask_env, env_secret_key",
    [
        (
            "dev",
            "",
        ),
        (
            "test",
            "",
        ),
        (
            "uat",
            "",
        ),
        (
            "production",
            "",
        ),
        ("db_migrations", ""),
        ("prod", ""),
    ],
)
def test_config_error(flask_env, env_secret_key):
    with mock.patch.dict(os.environ, {"SECRET_KEY": env_secret_key}):
        with pytest.raises(KeyError):
            CommonConfig._resolve_secret_key(flask_env)
