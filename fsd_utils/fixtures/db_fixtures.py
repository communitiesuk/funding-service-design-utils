from flask_migrate import upgrade
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import drop_database


def prep_db(reuse_db=False):
    """Provide the transactional fixtures with access to the database via a
    Flask-SQLAlchemy database connection."""

    from config import Config

    no_db = not database_exists(Config.SQLALCHEMY_DATABASE_URI)
    refresh_db = not reuse_db

    if no_db:

        create_database(Config.SQLALCHEMY_DATABASE_URI)

    elif refresh_db:

        drop_database(Config.SQLALCHEMY_DATABASE_URI)
        create_database(Config.SQLALCHEMY_DATABASE_URI)

    upgrade()
