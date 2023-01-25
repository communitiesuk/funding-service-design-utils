from datetime import datetime
from datetime import timedelta

from fsd_utils.config.commonconfig import CommonConfig


def test_get_default_round_id_before_w3(mocker):
    mocker.patch(
        "fsd_utils.config.commonconfig."
        + "current_datetime_after_given_iso_string",
        return_value=False,
    )
    default_round_id = CommonConfig.get_default_round_id()
    assert (
        CommonConfig.COF_ROUND_2_ID == default_round_id
    ), "Should be before W3 launch date"


def test_get_default_round_id_after_w3(mocker):
    mocker.patch(
        "fsd_utils.config.commonconfig."
        + "current_datetime_after_given_iso_string",
        return_value=True,
    )
    default_round_id = CommonConfig.get_default_round_id()
    assert (
        CommonConfig.COF_ROUND_2_W3_ID == default_round_id
    ), "Should be after W3 launch date"


def test_get_default_round_id_before_after_w3(monkeypatch):
    today = datetime.today().now()
    earlier = today - timedelta(hours=1)
    later = today + timedelta(hours=1)

    monkeypatch.setenv("COF_R2_W3_LAUNCH_TIME", str(later))

    default_round_id = CommonConfig.get_default_round_id()
    assert (
        CommonConfig.COF_ROUND_2_ID == default_round_id
    ), "Should be before W3 launch date"

    monkeypatch.setenv("COF_R2_W3_LAUNCH_TIME", str(earlier))

    default_round_id = CommonConfig.get_default_round_id()
    assert (
        CommonConfig.COF_ROUND_2_W3_ID == default_round_id
    ), "Should be after W3 launch date"
