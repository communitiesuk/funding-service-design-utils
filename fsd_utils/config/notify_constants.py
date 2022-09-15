class NotifyConstants:

    # ---- Required key Fields (DO NOT CHANGE) ----#
    FIELD_TYPE = "type"  # for TEMPLATE_TYPE.
    FIELD_CONTENT = "content"  # for contents to be shared.
    FIELD_TO = "to"  # for contact_info (do not set in common config)

    # ---- Template types constants (DO NOT CHANGE) ---#
    TEMPLATE_TYPE_MAGIC_LINK = "MAGIC_LINK"
    TEMPLATE_TYPE_APPLICATION = "APPLICATION_RECORD_OF_SUBMISSION"
    TEMPLATE_TYPE_NOTIFICATION = "NOTIFICATION"
    TEMPLATE_TYPE_REMINDER = "REMINDER"
    TEMPLATE_TYPE_AWARD = "AWARD"

    # Magic_Link Fields for FIELD_CONTENT #
    MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD = "contact_help_email"
    MAGIC_LINK_URL_FIELD = "magic_link_url"
    MAGIC_LINK_REQUEST_NEW_LINK_URL_FIELD = "request_new_link_url"
    MAGIC_LINK_FUND_NAME_FIELD = "fund_name"

    # Application Fields for FIELD_CONTENT #
    APPLICATION_SUBMISSION_DATE_FIELD = "date_submitted"
    APPLICATION_FUND_NAME_FIELD = "project_name"
    APPLICATION_ROUND_NAME_FIELD = "round_id"
    APPLICATION_ID_FIELD = "id"
