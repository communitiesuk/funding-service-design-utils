class NotifyConstants:

    # ---- Notification service endpoint ----#

    NOTIFICATION_SERVICE_ENDPOINT = "/send"

    # ---- Required keys Fields (DO NOT CHANGE) ----#

    FIELD_TYPE = "type"  # for TEMPLATE_TYPE.
    FIELD_CONTENT = "content"  # for contents to be shared.
    FIELD_TO = "to"  # for contact_info (do not set in common config)
    FIELD_FULL_NAME = "full_name"  # for contact_name (do not set in common config)

    # ---- Template types constants (DO NOT CHANGE) ---#

    TEMPLATE_TYPE_MAGIC_LINK = "MAGIC_LINK"
    TEMPLATE_TYPE_APPLICATION = "APPLICATION_RECORD_OF_SUBMISSION"
    TEMPLATE_TYPE_INCOMPLETE_APPLICATION = "INCOMPLETE_APPLICATION_RECORDS"
    TEMPLATE_TYPE_REMINDER = "APPLICATION_DEADLINE_REMINDER"
    TEMPLATE_TYPE_EOI_PASS = "Full pass"
    TEMPLATE_TYPE_EOI_PASS_W_CAVEATS = "Pass with caveats"
    TEMPLATE_TYPE_ASSESSMENT_APPLICATION_ASSIGNED = (
        "TEMPLATE_TYPE_ASSESSMENT_APPLICATION_ASSIGNED"
    )
    TEMPLATE_TYPE_ASSESSMENT_APPLICATION_UNASSIGNED = (
        "TEMPLATE_TYPE_ASSESSMENT_APPLICATION_UNASSIGNED"
    )

    # ---- Magic_Link Fields for FIELD_CONTENT ----#

    MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD = "contact_help_email"
    MAGIC_LINK_URL_FIELD = "magic_link_url"
    MAGIC_LINK_REQUEST_NEW_LINK_URL_FIELD = "request_new_link_url"
    MAGIC_LINK_FUND_NAME_FIELD = "fund_name"

    # ---- Application Fields for FIELD_CONTENT ----#

    APPLICATION_FIELD = "application"
    APPLICATION_FORMS_FIELD = "forms"
    APPLICATION_NAME_FIELD = "name"
    APPLICATION_QUESTIONS_FIELD = "questions"
    APPLICATION_CAVEATS = "caveats"

    # To be discussed with Gio/Jack/Adam

    # APPLICATION_SUBMISSION_DATE_FIELD = "date_submitted"
    # APPLICATION_FUND_NAME_FIELD = "project_name"
    # APPLICATION_ROUND_NAME_FIELD = "round_id"
    # APPLICATION_ID_FIELD = "id"
