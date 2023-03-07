import pytest


@pytest.fixture(autouse=True)
def clear_database(_db):
    """
    Fixture to clean up the database after each test.

    This fixture clears the database by deleting all data
    from tables and disabling foreign key checks before the test,
    and resetting foreign key checks after the test.

    Args:
    _db: The database instance.
    """
    yield

    # disable foreign key checks
    _db.session.execute("SET session_replication_role = replica")
    # delete all data from tables
    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    # reset foreign key checks
    _db.session.execute("SET session_replication_role = DEFAULT")
    _db.session.commit()
