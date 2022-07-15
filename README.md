# funding-service-design-utils
Shared library for funding service design apps.

This library can be installed into other python repos and the packages used by those repos.

# Releasing
To create a new release of funding-service-design-utils:
1. Make and test your changes as normal in this repo
2. Update the `version` tag in `setup.py`
3. Push your changes to `main`.
4. The Action at `.github/workflows/create-tag-workflow.yml` will create a new tag and release, named for the version in `setup.py`. This is triggered automatically on a push to main.

# Usage
Either of the following options will install the funding-service-design-utils into your python project. The package `fsd_utils` can then be imported.
## Tagged version
To reference a particular tag from pip, add the following to your `requirements.txt` file or use `pip install`:

    hhttps://github.com/communitiesuk/funding-service-design-utils/archive/refs/tags/<tagName>.tar.gz

## Latest / in-dev version
To reference the latest commit from a particular branch from pip, add the following to your `requirements.txt` file or use `pip install`:

    git+https://github.com/communitiesuk/funding-service-design-utils.git@<branchName>

# Utilities

## The configclass
Currently the configclass allows for pretty print debugging of config keys and the class from which they are created. This allows devs to quickly diagnoise problems arrising from incorrectly set config. To activate this functionality, one must decorate each config class with the `@configclass` decorator.

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
    SESSION_COOKIE_DOMAIN = "cloudapps.digital" # <--- This should be something specific and common to all microservices and the AUTHENTICATOR_HOST

NOTE: These values (and keys) need to be shared/common across all microservices that use each common authenticator host, and each microservice needs to be a subdomain of the SESSION_COOKIE_DOMAIN. If any of the environment *keys* for each of these attributes needs to be modified these can be reconfigured in fsd_utils/authentication/congfig.py.

Then - to use the `@login_required` decorator just add it to routes you need to protect eg:

    # in ...routes.py
    from fsd_utils.authentication.decorators import login_required

    @login_required
    def example_route(account_id):
        #...account_id will be available here if the user is authenticated
        #...if not logged in the user will be redirected to re-authenticate
