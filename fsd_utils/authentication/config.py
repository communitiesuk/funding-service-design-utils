"""
CONFIGURATION FOR SECURITY UTILITY

To use this utility please ensure that all the
"config_var_..." keys are set to the correct values
in the environment of the application that is using
this utility.
"""
config_var_auth_host = "AUTHENTICATOR_HOST"
config_var_user_token_cookie_name = "FSD_USER_TOKEN_COOKIE_NAME"
config_var_rs256_public_key = "RSA256_PUBLIC_KEY"
signout_route = "/sessions/sign-out"
