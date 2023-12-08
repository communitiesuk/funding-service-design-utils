import logging
import os


class CommonConfig:

    FSD_LOG_LEVELS = {
        "development": logging.DEBUG,
        "unit_test": logging.DEBUG,
        "dev": logging.INFO,
        "test": logging.WARN,
        "production": logging.ERROR,
    }

    # ---------------
    #  General App Config
    # ---------------
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "session_cookie")
    FLASK_ENV = os.getenv("FLASK_ENV")
    if not FLASK_ENV:
        raise KeyError("FLASK_ENV is not present in environment")
    try:
        FSD_LOG_LEVEL = FSD_LOG_LEVELS["FLASK_ENV"]
    except KeyError:
        FSD_LOG_LEVEL = FSD_LOG_LEVELS["production"]

    # ---------------
    # Dummy Hosts
    # ---------------

    TEST_ACCOUNT_STORE_API_HOST = "account_store"
    TEST_APPLICATION_STORE_API_HOST = "application_store"
    TEST_ASSESSMENT_STORE_API_HOST = "assessment_store"
    TEST_FUND_STORE_API_HOST = "fund_store"
    TEST_NOTIFICATION_SERVICE_HOST = "notification_service"

    # ---------------
    #  Account hosts, endpoints
    # ---------------

    ACCOUNT_STORE_API_HOST = os.getenv(
        "ACCOUNT_STORE_API_HOST", TEST_ACCOUNT_STORE_API_HOST
    )
    ACCOUNTS_ENDPOINT = "/accounts"
    ACCOUNT_ENDPOINT = "/accounts/{account_id}"

    # ---------------
    #  Application hosts, endpoints
    # ---------------

    APPLICATION_STORE_API_HOST = os.getenv(
        "APPLICATION_STORE_API_HOST", TEST_APPLICATION_STORE_API_HOST
    )
    APPLICATIONS_ENDPOINT = "/applications"
    APPLICATION_ENDPOINT = "/applications/{application_id}"
    APPLICATION_STATUS_ENDPOINT = "/applications/{application_id}/status"
    APPLICATION_SEARCH_ENDPOINT = "/applications?{params}"

    # ---------------
    # Assessment hosts, endpoints
    # ---------------

    ASSESSMENT_STORE_API_HOST = os.getenv(
        "ASSESSMENT_STORE_API_HOST", TEST_ASSESSMENT_STORE_API_HOST
    )

    # ---------------
    #  Fund hosts, endpoints
    # ---------------

    FUND_STORE_API_HOST = os.getenv("FUND_STORE_API_HOST", TEST_FUND_STORE_API_HOST)
    FUNDS_ENDPOINT = "/funds"
    FUND_ENDPOINT = "/funds/{fund_id}"  # account id in assessment store

    ROUNDS_ENDPOINT = "/funds/{fund_id}/rounds"
    ROUND_ENDPOINT = "/funds/{fund_id}/rounds/{round_id}"

    # ---------------
    #  Notification hosts, endpoints, fields
    # ---------------

    NOTIFICATION_SERVICE_HOST = os.getenv("NOTIFICATION_SERVICE_HOST")
    NOTIFICATION_SEND_ENDPOINT = "/send"

    # ---------------
    #  SESSION TIMELIMITS
    # ---------------

    FSD_SESSION_TIMEOUT_SECONDS = 86400  # (24hrs)
    WTF_CSRF_TIME_LIMIT = FSD_SESSION_TIMEOUT_SECONDS + 10  # (buffer secconds)

    # ---------------
    #  Talisman Settings
    # ---------------

    # Allow inline scripts for swagger docs (for Talisman Config)
    SWAGGER_CSP = {
        "script-src": ["'self'", "'unsafe-inline'"],
        "style-src": ["'self'", "'unsafe-inline'"],
    }

    # Content Security Policy
    SECURE_CSP = {
        "default-src": "'self'",
        "script-src": [
            "'self'",
            "'sha256-+6WnXIl4mbFTCARd8N3COQmT3bJJmo32N8q8ZSQAIcU='",
            "'sha256-l1eTVSK8DTnK8+yloud7wZUqFrI0atVo6VlC6PJvYaQ='",
            "'sha256-864+qKuyx4sP6oZXnPPGzxGuBEHMZ132TQ4RPp+zn44='",
            "'sha256-Z4Ew9hvNfnmh80vfWPHh13YzZdj0gTwoY6COVqIdaV0='",
            "'sha256-z+p4q2n8BOpGMK2/OMOXrTYmjbeEhWQQHC3SF/uMOyg='",
            "'sha256-RgdCrr7A9yqYVstE6QiM/9RNRj4bYipcUa2C2ywQT1A='",
            "https://tagmanager.google.com",
            "https://www.googletagmanager.com",
            "https://*.google-analytics.com",
        ],
        "connect-src": [
            "'self'",
            "https://*.google-analytics.com",
        ],  # APPLICATION_STORE_API_HOST_PUBLIC,
        "img-src": ["data:", "'self'", "https://ssl.gstatic.com"],
    }

    # Security headers and other policies
    FSD_REFERRER_POLICY = "strict-origin-when-cross-origin"
    FSD_SESSION_COOKIE_SAMESITE = "Lax"
    FSD_PERMISSIONS_POLICY = {"interest-cohort": "()"}
    FSD_DOCUMENT_POLICY = {}
    FSD_FEATURE_POLICY = {
        "microphone": "'none'",
        "camera": "'none'",
        "geolocation": "'none'",
    }

    DENY = "DENY"
    SAMEORIGIN = "SAMEORIGIN"
    ALLOW_FROM = "ALLOW-FROM"
    ONE_YEAR_IN_SECS = 31556926

    FORCE_HTTPS = False

    TALISMAN_SETTINGS = {
        "feature_policy": FSD_FEATURE_POLICY,
        "permissions_policy": FSD_PERMISSIONS_POLICY,
        "document_policy": FSD_DOCUMENT_POLICY,
        "force_https": FORCE_HTTPS,
        "force_https_permanent": False,
        "force_file_save": False,
        "frame_options": "SAMEORIGIN",
        "frame_options_allow_from": None,
        "strict_transport_security": True,
        "strict_transport_security_preload": True,
        "strict_transport_security_max_age": ONE_YEAR_IN_SECS,
        "strict_transport_security_include_subdomains": True,
        "content_security_policy": SECURE_CSP,
        "content_security_policy_report_uri": None,
        "content_security_policy_report_only": False,
        "content_security_policy_nonce_in": None,
        "referrer_policy": FSD_REFERRER_POLICY,
        "session_cookie_secure": True,
        "session_cookie_http_only": True,
        "session_cookie_samesite": FSD_SESSION_COOKIE_SAMESITE,
        "x_content_type_options": True,
        "x_xss_protection": True,
    }

    FSD_LANG_COOKIE_NAME = "language"

    # ---------------
    #  Feature Toggles
    # ---------------

    dev_feature_configuration = {"MULTIFUND_DASHBOARD": True}

    prod_feature_configuration = {"MULTIFUND_DASHBOARD": True}
