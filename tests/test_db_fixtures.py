pytest_plugins = ["pytester"]


def test_spam(pytester, mocker):
    pytester.copy_example("test_spam_fixture.py")
    mocker.patch(
        "fsd_utils.fixtures.db_fixtures.upgrade",
        new=lambda _: print("upgrading"),
    )
    result = pytester.runpytest("-k", "test_spam_fixture")
    result.assert_outcomes(passed=1)
