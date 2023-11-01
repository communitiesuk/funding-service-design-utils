"""
CONFIGURATION FOR SECURITY UTILITY

To use this utility please ensure that all the
"config_var_..." keys are set to the correct values
in the environment of the application that is using
this utility.
"""
import enum

config_var_auth_host = "AUTHENTICATOR_HOST"
config_var_logout_url_override = "LOGOUT_URL_OVERRIDE"
config_var_user_token_cookie_name = "FSD_USER_TOKEN_COOKIE_NAME"
config_var_rs256_public_key = "RSA256_PUBLIC_KEY"
signout_route = "/sessions/sign-out"
user_route = "/service/user"


class SupportedApp(enum.Enum):
    POST_AWARD_FRONTEND = "post-award-frontend"
    POST_AWARD_SUBMIT = "post-award-submit"
