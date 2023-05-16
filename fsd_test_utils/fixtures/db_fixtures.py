import pytest
from flask_migrate import upgrade
from sqlalchemy import text
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import drop_database


def prep_db(reuse_db=False):
    """
    Determines whether the target database already exists, if it
    doesn't it is created.
    If it exists but reuse_db is False, then the DB is dropped and recreated.
    upgrade() is always run to make sure the schema is up to date.
    """

    from config import Config

    no_db = not database_exists(Config.SQLALCHEMY_DATABASE_URI)
    refresh_db = not reuse_db

    if no_db:
        create_database(Config.SQLALCHEMY_DATABASE_URI)

    elif refresh_db:
        drop_database(Config.SQLALCHEMY_DATABASE_URI)
        create_database(Config.SQLALCHEMY_DATABASE_URI)

    upgrade()


@pytest.fixture(scope="session")
def _db(app, request):
    """
    Fixture to supply tests with direct access to the database
    """
    yield app.extensions["sqlalchemy"]


@pytest.fixture(scope="session")
def recreate_db(request, _db, app):
    """
    Fixture to determine whether we need to clear out the existing DB
    (based on cache values) and then call prep_db.
    This is session scoped so we only drop/create the db
    at the start of a test session
    """
    print("Recreating db")
    reuse_db = bool(request.config.cache.get("reuse_db", False))
    with app.app_context():
        prep_db(reuse_db)
    request.config.cache.set("reuse_db", True)
    yield


@pytest.fixture(scope="session")
def clear_test_data(app, _db, request, recreate_db):
    """
    Fixture to clean up the database after each test.

    This fixture reads preserve_test_data from the cache
    (see enable_preserve_test_data below),
    and if we are not preserving the data it clears the database
    by deleting all data from all tables.

    This is module scoped so that each test file gets a fresh empty
    database.

    """
    with app.app_context():
        yield
        preserve_test_data = request.config.cache.get("preserve_test_data", None)
        if not preserve_test_data:
            # rollback incase of any errors during test session
            _db.session.rollback()
            # disable foreign key checks
            _db.session.execute(text("SET session_replication_role = replica"))
            # delete all data from tables
            for table in reversed(_db.metadata.sorted_tables):
                _db.session.execute(table.delete())
            # reset foreign key checks
            _db.session.execute(text("SET session_replication_role = DEFAULT"))
            _db.session.commit()
        else:
            # If test requests 'preserve test data' make sure
            # on the next run we clear out the DB completely.
            request.config.cache.set("reuse_db", False)
            request.config.cache.set("preserve_test_data", False)


@pytest.fixture(scope="function")
def enable_preserve_test_data(request):
    """
    Fixture to read the markers on a test and if preserve_test_data is
    set, it sets it in the cache.
    This can't be combined with clear_test_data due to conflicts on the fixture
    scope, so this function reads the test markers and clear_test_data
    reads the cache.
    """
    marker = request.node.get_closest_marker("preserve_test_data")
    if marker is not None:
        request.config.cache.set("preserve_test_data", True)
