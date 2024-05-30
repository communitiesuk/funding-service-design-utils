from uuid import uuid4

from fsd_utils.services.aws_sqs_extended_client_exception import ExceptionMessages
from fsd_utils.services.aws_sqs_extended_client_exception import (
    SQSExtendedClientException,
)

S3_KEY_ATTRIBUTE_NAME = "S3Key"
MAX_ALLOWED_ATTRIBUTES = 10 - 1  # 10 for SQS and 1 reserved attribute
DEFAULT_MESSAGE_SIZE_THRESHOLD = 262144
RESERVED_ATTRIBUTE_NAME = "ExtendedPayloadSize"
MESSAGE_POINTER_CLASS = "software.amazon.payloadoffloading.PayloadS3Pointer"


def get_message_attributes_size(message_attributes: dict) -> int:
    """
    Responsible for calculating the size, in bytes, of the message attributes
    of a given message payload
    :message_attributes: A dictionary consisting of message attributes.
    Each message attribute consists of the name (key) along with a
    type and value of the message body. The following types are supported
    for message attributes: StringValue, BinaryValue and DataType.
    """
    total_message_attributes_size = 0
    for key, value in message_attributes.items():
        total_message_attributes_size += len(key.encode("utf-8"))

        datatype_value = value.get("DataType", 0)
        if datatype_value:
            total_message_attributes_size += len(key.encode("utf-8"))

        stringtype_value = value.get("StringValue", 0)
        if stringtype_value:
            total_message_attributes_size += len(key.encode("utf-8"))

        binary_type_value = value.get("BinaryValue", 0)
        if binary_type_value:
            total_message_attributes_size += len(key.encode("utf-8"))

    return total_message_attributes_size


def get_reserved_attribute_name_if_present(message_attributes: dict) -> str:
    """
    Responsible for checking the reserved message attribute, SQSLargePayloadSize
    or ExtendedPayloadSize in this specific case, exists in the
    message_attributes
    :message_attributes: A dictionary consisting of message attributes.
    Each message attribute consists of the name (key) along with a
    type and value of the message body. The following types are supported
    for message attributes: StringValue, BinaryValue and DataType.
    """
    reserved_attribute_name = ""
    if RESERVED_ATTRIBUTE_NAME in message_attributes:
        reserved_attribute_name = RESERVED_ATTRIBUTE_NAME
    return reserved_attribute_name


def check_message_attributes(message_attributes: dict) -> None:
    """
    Responsible for checking the constraints on the message attributes
    for a given message
    :message_attributes A dictionary consisting of message attributes.
    Each message attribute consists of the name (key) along with a
    type and value of the message body. The following types are supported
    for message attributes: StringValue, BinaryValue and DataType.
    """
    total_message_attributes_size = get_message_attributes_size(message_attributes)

    if total_message_attributes_size > DEFAULT_MESSAGE_SIZE_THRESHOLD:
        raise SQSExtendedClientException(
            ExceptionMessages.INVALID_MESSAGE_ATTRIBUTE_SIZE.format(
                total_message_attributes_size, DEFAULT_MESSAGE_SIZE_THRESHOLD
            )
        )

    message_attributes_num = len(message_attributes)
    if message_attributes_num > MAX_ALLOWED_ATTRIBUTES:
        raise SQSExtendedClientException(
            ExceptionMessages.INVALID_NUMBER_OF_MESSAGE_ATTRIBUTES.format(
                message_attributes_num, MAX_ALLOWED_ATTRIBUTES
            )
        )

    reserved_attribute_name = get_reserved_attribute_name_if_present(message_attributes)
    if reserved_attribute_name:
        raise SQSExtendedClientException(
            ExceptionMessages.INVALID_ATTRIBUTE_NAME_PRESENT.format(
                reserved_attribute_name
            )
        )

    return


def get_s3_key(message_attributes: dict, extra_attributes: dict) -> str:
    """
    Responsible for checking if the S3 Key exists in the
    message_attributes
    :message_attributes: A dictionary consisting of message attributes
    :extra_attributes: A dictionary consisting of message attributes
    Each message attribute consists of the name (key) along with a
    type and value of the message body. The following types are supported
    for message attributes: StringValue, BinaryValue and DataType.
    """

    if S3_KEY_ATTRIBUTE_NAME in message_attributes:
        return message_attributes[S3_KEY_ATTRIBUTE_NAME]["StringValue"]
    elif extra_attributes and S3_KEY_ATTRIBUTE_NAME in extra_attributes:
        return (
            extra_attributes[S3_KEY_ATTRIBUTE_NAME]["StringValue"] + "/" + str(uuid4())
        )
    return str(uuid4())


def validate_messages(messages):
    for msg in messages:
        if not msg["MessageId"] and not msg["ReceiptHandle"] and not msg["Body"]:
            raise SQSExtendedClientException(
                ExceptionMessages.INVALID_ARGUMENTS_FOR_DELETE_MESSAGE
            )
