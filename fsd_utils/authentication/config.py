"""
CONFIGURATION FOR SECURITY UTILITY

To use this utility please ensure that all the
"config_var_..." keys are set to the correct values
in the environment of the application that is using
this utility.
"""
import enum

config_var_auth_host = "AUTHENTICATOR_HOST"
config_var_user_token_cookie_name = "FSD_USER_TOKEN_COOKIE_NAME"
config_var_rs256_public_key = "RSA256_PUBLIC_KEY"
signout_route = "/sessions/sign-out"
user_route = "/service/user"
azure_ad_role_map = {
    # deprecated roles
    "LeadAssessor": "COF_LEAD_ASSESSOR",
    "Assessor": "COF_ASSESSOR",
    "Commenter": "COF_COMMENTER",
    # COF specific roles
    "COF_Lead_Assessor": "COF_LEAD_ASSESSOR",
    "COF_Assessor": "COF_ASSESSOR",
    "COF_Commenter": "COF_COMMENTER",
    "COF_England": "COF_ENGLAND",
    "COF_NorthernIreland": "COF_NORTHERNIRELAND",  # TODO: what did they call this?
    "COF_Scotland": "COF_SCOTLAND",
    "COF_Wales": "COF_WALES",
    # NSTF specific roles
    "NSTF_Lead_Assessor": "NSTF_LEAD_ASSESSOR",
    "NSTF_Assessor": "NSTF_ASSESSOR",
    "NSTF_Commenter": "NSTF_COMMENTER",
}


class SupportedApp(enum.Enum):
    POST_AWARD_FRONTEND = "post-award-frontend"
    POST_AWARD_SUBMIT = "post-award-submit"
