from fsd_utils.config.commonconfig import CommonConfig


def test_get_default_round_id_before_w3(mocker):
    mocker.patch(
        "fsd_utils.config.commonconfig.get_remote_data_as_json",
        return_value={"opens": "2029-01-01"},
    )
    default_round_id = CommonConfig.get_default_round_id()
    assert (
        CommonConfig.COF_ROUND_2_ID == default_round_id
    ), "Should be before W3 launch date"


def test_get_default_round_id_after_w3(mocker):
    mocker.patch(
        "fsd_utils.config.commonconfig.get_remote_data_as_json",
        return_value={"opens": "2023-01-01"},
    )
    default_round_id = CommonConfig.get_default_round_id()
    assert (
        CommonConfig.COF_ROUND_2_W3_ID == default_round_id
    ), "Should be after W3 launch date"
