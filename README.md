# funding-service-design-utils
Utils serves as a shared library for funding service design applications. These utilities are meant to be reused across the project, streamlining our coding process and ensuring the reliability of our funding service design applications.

This library can be installed into other python repos and the packages used by those repos.

This service depends on:
- No other microservices

# Dev setup
In order to run the unit tests, setup a virtual env and install requirements
[Developer setup guide](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-setup.md)

Install pre-commit hook: https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-ide-setup.md

If you add any packages needed by services that consume `fsd_utils`, add them into `pyproject.yaml`.

# Testing

Tests in this repository run using `pytest`, as per our standardise [Testing in Python repos](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-testing.md) practice.

However, because this is a shared utils library that can be installed under different conditions (mainly Python or Flask versions), we matrix test the combinations using [tox](https://tox.wiki/en/4.15.1/).

To setup tox for use with `uv`:

```bash
uv tool install tox~=4.0 --with tox-uv
tox --version  # check that you are using a tox with the tox-uv plugin installed
```

To run tests via tox, `tox`. To run suites in parallel, run eg `tox -p 8`.

# Releasing
To create a new release of funding-service-design-utils (note no longer need to manually update the version):
1. Make and test your changes as normal in this repo
1. Push your changes to `main`.
1. The Action at `.github/workflows/test-and-tag.yml` will create a new tag and release, named for the version in `pyproject.toml`. This is triggered automatically on a push to main.
1. That action will also push this tag up to PyPI at: https://pypi.org/project/funding-service-design-utils/

## Updating the release workflow
- If making changes to the release flow etc, you can publish to test.pypi.org when testing. To do this, update the `Publish to PyPI` step with the following:
```
    - name: Publish to PyPI
      id: publish-to-pypi
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN_TEST }}
        repository_url: https://test.pypi.org/legacy/
```
- That will publish packages to https://test.pypi.org/project/funding-service-design-utils/ instead, without updating the index of the main PyPI repo.
- Don't forget to change it back when you're done!

# Usage
Either of the following options will install the funding-service-design-utils into your python project. The package `fsd_utils` can then be imported.

## Released version
To install a particular version, use `uv add funding-service-design-utils==0.0.1` (update the version number as appropriate).

## Latest / in-dev version
To reference the latest commit from a particular branch:

    uv add git+https://github.com/communitiesuk/funding-service-design-utils --branch <branch_name>

Build docker with following commands

    docker compose build <service_name> --no-cache

or

    docker compose build --no-cache

## Local changes
When working and testing locally, you can also install the `fsd_utils` package from your local filesystem:

    uv remove funding-service-design-utils
    uv add /path/to/your/working/directory/funding-service-design/utils

Note: When testing locally using the docker runner, docker might use the cached version of fsd_utils. To avoid this and pick up your intended changes, run `docker compose build <service_name> --no-cache` first before running `docker compose up`. Docker will not be able to use your local checkout of utils.

# Utilities

## The configclass
Currently the configclass allows for pretty print debugging of config keys and the class from which they are created. This allows devs to quickly diagnoise problems arrising from incorrectly set config. To activate this functionality, one must decorate each config class with the `@configclass` decorator.

## Common Config
This defines config values that are common across different services, eg. url patterns. Usage example:

```
from fsd_utils import CommonConfig

@configclass
class DefaultConfig:
    SECRET_KEY = CommonConfig.SECRET_KEY

```


## Gunicorn
The gunicorn utility allows consistent configuration of gunicorn across microservices.

To use it,
First - add run/gunicorn directory in your application with config scripts that import the appropriate config from this util's choice of config files eg.

    # in run/gunicorn/local.py
    from fsd_utils.gunicorn.config.local import *  # noqa

Then - add a wsgi.py script to the root of your application eg.

    # in wsgi.py
    from app import app

    if __name__ == "__main__":
        app.run()

Finally - To run with gunicorn, call the gunicorn command in your manifest.yml's or in the terminal, passing the wsgi application and the appropriate configuration file as arguments eg.

in the terminal:

    gunicorn wsgi:app -c run/gunicorn/dev.py

in a manifest file:

    # manifest-dev.yml
    ---
    applications:
        ...
        command: gunicorn wsgi:app -c run/gunicorn/devtest.py

## Logging
The logging utility formats logs to a consistent format (text in development and json in other environments).
The utility also supports logging from gunicorn

To use it add the following to your flask create_app factory

    from fsd_utils.logging import logging

    def create_app():
        ...
        # Initialise logging
        logging.init_app(flask_app)

and in your env config classes, specify the log level you want to report eg.:

    @configclass
    class DefaultConfig(object):
        ...
        # Logging
        FSD_LOG_LEVEL = logging.WARNING

## Authentication
The authentication utility provides a consistent authentication functions including a `@login_required` decorator that can be used to restrict routes that should only be accessible to authenticated users.

To use the utility:
First - ensure that the following environment variables are set to the appropriate values eg.:

    FSD_USER_TOKEN_COOKIE_NAME = "fsd_user_token"
    AUTHENTICATOR_HOST = "https://funding-service-design-authenticator-dev.london.cloudapps.digital"
    RSA256_PUBLIC_KEY = "{RSA PUBLIC KEY}"

NOTE: These values (and keys) need to be shared/common across all microservices that use each common authenticator host. If any of the environment *keys* for each of these attributes needs to be modified these can be reconfigured in fsd_utils/authentication/config.py.

To generate new keys in your cwd, you use the following commands:
```bash
openssl genrsa -out private_key.pem 2048
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

If you're changing keys, you'll need to change them in GitHub secrets across repos.
Please also add them to BitWarden and let the team know.


Then - to use the `@login_required` decorator just add it to routes you need to protect eg:

    # in ...routes.py
    from fsd_utils.authentication.decorators import login_required

    @login_required
    def example_route(account_id):
        #...account_id will be available here if the user is authenticated
        #...if not logged in the user will be redirected to re-authenticate

## Healthchecks
Adds the route `/healthcheck` to an application. On hitting this endpoint, a customisable set of checks are run to confirm the application is functioning as expected and a JSON response is returned.

Response codes:
- 200: All checks were successful, application is healthy
- 500: One or more checks failed, application is unhealthy

Example usage:
```
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.healthchecks.checkers import DbChecker, FlaskRunningChecker

health = Healthcheck(flask_app)
health.add_check(FlaskRunningChecker())
health.add_check(DbChecker(db))
```
The above will initialise the `/healthcheck` url and adds 2 checks.

### Checks
The following 2 checks are provided in `fsd_utils` in `checkers.py`:
- `FlaskRunningChecker`: Checks whether a `current_app` is available from flask, returns `True` if it is, `False` if not.
- `DbChecker`: Runs a simple query against the DB to confirm database availability.

### Implementing custom checks
Custom checks can be created as subclasses of `CheckerInterface` and should contain a method with the following signature:
`def check(self) -> Tuple[bool, str]:`
Where
- `bool` is a True or False whether the check was successful
- `str` is a message to display in the result JSON, typically `OK` or `Fail`

## Sentry
Enables Sentry integration.

* Before the flask app is created initialise Sentry using
```
from fsd_utils import init_sentry

init_sentry()
```
* Set the `SENTRY_DSN` environment variable on the app

## Simple Utils
Folder to hold miscellaneous simple utilities.

### date_utils
Date comparison functions that accept an ISO Format string, for use in the frontend determining display logic based on dates.

## Fixtures
Contains shared fixtures that can be used for unit tests in other repos. To include a fixture from `fsd_utils` in your project, add the following to your `conftest.py`:

    pytest_plugins = ["fsd_test_utils.fixtures.db_fixtures"]

Where the part inside `[]` is the paths to the python files you want to load as fixtures.

### DB_Fixtures

Individual fixtures are explained below, but this is the general expected usage. In the `conftest.py` of your repo, define a fixture that will seed the database with the test data you require and make those records avaialble to tests. That fixture should request `clear_test_data` and `enable_preserve_test_data` to prevent test pollution and ensure a suitable database is available for tests. The tests themselves should only update data that is inserted by that fixture. Examples:

1. Basic Usage

    In conftest.py

        @pytest.fixture(scope="function")
        def create_test_data(clear_test_data, enable_preserve_test_data):
            # Logic to insert some test data
            created_data = [all_created_data]

            yield created_data

            # No teardown logic required as this is covered in clear_test_data

    In your test file

        def test_get_data(create_test_data):
            id = create_test_data[0].id
            record = get_record_using_api_under_test(id)
            assert record.id == id

1. If your tests need to directly manipulate the database, use the `_db` fixture:

        def test_after_update(create_test_data, _db):
            id = create_test_data[0].id
            record = get_record(id)
            record.name = "new name"

            _db.session.add(record)
            _db.session.commit()

            # Do some further tests post update

1. If you want to be able to inspect the database after running a test:

        @pytest.mark.preserve_test_data(True)
        def test_get_data(create_test_data):
            id = create_test_data[0].id
            record = get_record_using_api_under_test(id)
            assert record.id == id

    After the test runs, any created data will still be there for manual inspection. It will then be removed at the start of the next test run.

#### clear_test_data
This fixture is module scoped so at the end of each test file all data is removed from the database (providing `preserve_test_data` is not set - see below.) Helps to prevent test pollution.
#### enable_preserve_test_data
This fixture looks for the marker `pytest.mark.preserve_test_data(True)` and if found, test data is not cleared at the end of the test session, allowing you to manually inspect the database to aid debugging.

**Note**: Not intended to be used as a default for tests as it can lead to test pollution, so only use to debug and then remove again.
#### _db
Provides direct access to the database for tests. Useful if your test needs to explicitly insert/update records to prepare test data.
#### recreate_db
This fixture reads the pytest cache to determine whether the DB can be reused for this test run and then the db is recreated accordingly. Updates the cache value to enable reuse of the DB for future test runs. This is session scoped so the DB is not recreated for each test in a run.

This is requested by `clear_test_data` so you do not need to include it separately in your project if using that fixture.



## Mapping

The mapping feature serves the purpose of mapping and formatting the questions and answers of the application into a text file. This functionality is utilised in the following scenarios:

- Within the assessment service, it facilitates the downloading of the application's questions and answers.
- In the notification service, it enables the posting of the applicant's application answer.

To accomplish the mapping of the application's questions and answers, import

    from fsd_utils import extract_questions_and_answers

To format the questions and answers of the application into a text file, import

    from fsd_utils import generate_text_of_application
