from botocore.exceptions import BotoCoreError


class SQSExtendedClientException(BotoCoreError):
    """
    Base Class for all SQS Extended Client exceptions which occur
    after interacting with the SQS Extended Client.
    """

    def __init__(self, error_message):
        self.fmt = error_message
        super().__init__()


class ExceptionMessages:
    INVALID_ARGUMENTS_FOR_DELETE_MESSAGE = (
        "Invalid number of arguments while calling delete_message."
    )
    INVALID_MESSAGE_ATTRIBUTE_SIZE = (
        "Total size of message attributes is {0} bytes which is larger than the "
        "threshold of {1} bytes. Consider including the payload in the message body "
        "instead of the message attributes."
    )
    INVALID_NUMBER_OF_MESSAGE_ATTRIBUTES = (
        "Number of message attributes {0} exceeds the maximum allowed for "
        "large-payload messages {1}"
    )
    INVALID_ATTRIBUTE_NAME_PRESENT = (
        "Message attribute name {0} is reserved for use by the SQS extended client. "
    )
    INVALID_MESSAGE_BODY = "messageBody cannot be null or empty."
    INVALID_FORMAT_WHEN_RETRIEVING_STORED_S3_MESSAGES = (
        "Invalid payload format for retrieving stored messages in S3"
    )

    FAILED_DELETE_MESSAGE = "delete_object failed with status code {0}"
    FAILED_SUBMIT_MESSAGE = "submit_single_message failed with status code {0}"
    FAILED_RECEIVE_MESSAGE = "receive_messages failed with status code {0}"
