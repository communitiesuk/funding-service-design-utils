pytest_plugins = ["fsd_utils.fixtures.db_fixtures"]


def test_spam_fixture(mocker, spam):
    mocker.patch(
        "fsd_utils.fixtures.db_fixtures.upgrade",
        new=lambda _: print("upgrading"),
    )
    assert "eggs" == spam
