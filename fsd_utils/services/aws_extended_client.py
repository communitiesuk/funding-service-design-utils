import json
from datetime import datetime

import boto3
from fsd_utils.services.aws_sqs_extended_client_exception import ExceptionMessages
from fsd_utils.services.aws_sqs_extended_client_exception import (
    SQSExtendedClientException,
)
from fsd_utils.services.aws_sqs_extended_client_util import check_message_attributes
from fsd_utils.services.aws_sqs_extended_client_util import get_s3_key
from fsd_utils.services.aws_sqs_extended_client_util import MESSAGE_POINTER_CLASS
from fsd_utils.services.aws_sqs_extended_client_util import RESERVED_ATTRIBUTE_NAME
from fsd_utils.services.aws_sqs_extended_client_util import validate_messages


class SQSExtendedClient:
    def __init__(
        self,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        region_name="eu-west-2",
        endpoint_url=None,
        large_payload_support=None,
        always_through_s3=None,
        delete_payload_from_s3=None,
        logger=None,
        **kwargs,
    ):
        self.large_payload_support = large_payload_support
        self.always_through_s3 = always_through_s3
        self.delete_payload_from_s3 = delete_payload_from_s3
        self.logger = logger

        if aws_access_key_id and aws_secret_access_key:
            self.sqs_client = boto3.client(
                "sqs",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
                endpoint_url=endpoint_url,
                **kwargs,
            )
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
                endpoint_url=endpoint_url,
            )
        else:
            """
            if 'aws_access_key_id' and 'aws_access_key_id' are not provided make sure to provide
            'AWS_ACCESS_KEY_ID' and 'AWS_SECRET_ACCESS_KEY' with environment variables
            """
            self.sqs_client = boto3.client(
                "sqs",
                region_name=region_name,
                endpoint_url=endpoint_url,
                **kwargs,
            )
            self.s3_client = boto3.client(
                "s3",
                region_name=region_name,
                endpoint_url=endpoint_url,
            )

    def get_queues(self, prefix=None):
        """
        Gets a list of SQS queues. When a prefix is specified, only queues with names
        that start with the prefix are returned.

        :param prefix: The prefix used to restrict the list of returned queues.
        :return: A list of Queue names.
        """
        if prefix:
            return self._get_queue_names(
                self.sqs_client.list_queues(QueueNamePrefix=prefix)["QueueUrls"]
            )
        return self._get_queue_names(self.sqs_client.list_queues()["QueueUrls"])

    def submit_single_message(
        self,
        queue_url,
        message,
        extra_attributes: dict = None,
        message_group_id=None,
        message_deduplication_id=None,
    ):
        sqs_message_attributes = {
            "message_created_at": {
                "StringValue": str(datetime.now()),
                "DataType": "String",
            },
        }
        message_body, message_attributes = self._store_message_in_s3(
            message, sqs_message_attributes, extra_attributes
        )
        # add extra message attributes (if provided)
        if extra_attributes:
            for key, value in extra_attributes.items():
                message_attributes[key] = value

        response = self.sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes=message_attributes,
            MessageGroupId=message_group_id,
            MessageDeduplicationId=message_deduplication_id,
        )
        # Check if the delete operation succeeded, if not raise an error?
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code != 200:
            raise SQSExtendedClientException(
                ExceptionMessages.FAILED_SUBMIT_MESSAGE.format(status_code)
            )
        message_id = response["MessageId"]
        self.logger.info(f"Called SQS and submitted the message and id [{message_id}]")
        return message_id

    def receive_messages(self, queue_url, max_number, visibility_time=1, wait_time=1):
        """
        Receive a batch of messages in a single request from an SQS queue.
        :param queue_url: SQS Queue url
        :param max_number: The maximum number of messages to receive. The actual number
                        of messages received might be less.
        :param visibility_time: The maximum time for message to temporarily invisible to other receivers.
                                This gives the initial receiver a chance to process the message. If the receiver
                                successfully processes and deletes the message within the visibility timeout,
                                the message is removed from the queue.
        :param wait_time: The maximum time to wait (in seconds) before returning. When
                        this number is greater than zero, long polling is used. This
                        can result in reduced costs and fewer false empty responses.
        :return: The list of Message objects received. These each contain the body
                of the message and metadata and custom attributes.
        """
        response = self.sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=["SentTimestamp", "ApproximateReceiveCount"],
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_number,
            VisibilityTimeout=visibility_time,
            WaitTimeSeconds=wait_time,
        )

        # Check if the delete operation succeeded, if not raise an error?
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code != 200:
            raise SQSExtendedClientException(
                ExceptionMessages.FAILED_RECEIVE_MESSAGE.format(status_code)
            )
        messages = []
        if "Messages" in response.keys():
            messages = response["Messages"]
            self.logger.info(f"Called SQS and received [{len(messages)}] messages")
        elif response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return []

        if self.large_payload_support and self.always_through_s3:
            extended_message = []
            for msg in messages:
                dict_msg = {
                    "sqs": msg,
                    "s3": self._retrieve_message_from_s3(msg["Body"]),
                }
                extended_message.append(dict_msg)
            return extended_message
        return messages

    def delete_messages(self, queue_url, messages):
        validate_messages(messages)
        reciept_handles_to_delete = []
        if self.large_payload_support and self.always_through_s3:
            return self._delete_msg_from_sqs_and_s3(
                messages, queue_url, reciept_handles_to_delete
            )
        return self._delete_msg_from_sqs(messages, queue_url, reciept_handles_to_delete)

    def _delete_msg_from_sqs_and_s3(
        self, messages, queue_url, reciept_handles_to_delete
    ):
        self._delete_message_from_s3(messages, reciept_handles_to_delete)
        entries = [
            {"Id": str(ind), "ReceiptHandle": receipt_handle}
            for ind, receipt_handle in enumerate(reciept_handles_to_delete)
        ]
        response = self.sqs_client.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )
        # Check if the delete operation succeeded, if not raise an error?
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code != 200:
            raise SQSExtendedClientException(
                ExceptionMessages.FAILED_DELETE_MESSAGE.format(status_code)
            )
        self.logger.info("Called SQS and deleted the message")
        if "Successful" in response:
            for msg_meta in response["Successful"]:
                self.logger.info(
                    f"Deleted {reciept_handles_to_delete[int(msg_meta['Id'])]}"
                )
        if "Failed" in response:
            for msg_meta in response["Failed"]:
                self.logger.info(
                    f"Could not delete {reciept_handles_to_delete[int(msg_meta['Id'])]}"
                )
        return response

    def _delete_msg_from_sqs(self, messages, queue_url, reciept_handles_to_delete):
        for message in messages:
            reciept_handles_to_delete.append(message["ReceiptHandle"])
        entries = [
            {"Id": str(ind), "ReceiptHandle": receipt_handle}
            for ind, receipt_handle in enumerate(reciept_handles_to_delete)
        ]
        response = self.sqs_client.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )
        # Check if the delete operation succeeded, if not raise an error?
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code != 200:
            raise SQSExtendedClientException(
                ExceptionMessages.FAILED_DELETE_MESSAGE.format(status_code)
            )
        self.logger.info("Called SQS and deleted the message")
        if "Successful" in response:
            for msg_meta in response["Successful"]:
                self.logger.info(
                    f"Deleted {reciept_handles_to_delete[int(msg_meta['Id'])]}"
                )
        if "Failed" in response:
            for msg_meta in response["Failed"]:
                self.logger.info(
                    f"Could not delete {reciept_handles_to_delete[int(msg_meta['Id'])]}"
                )
        return response

    def _delete_message_from_s3(self, messages, reciept_handles_to_delete):
        for msg in messages:
            message_body = json.loads(msg["Body"])
            reciept_handles_to_delete.append(msg["ReceiptHandle"])
            if not (
                isinstance(message_body, list)
                and len(message_body) == 2
                and isinstance(message_body[1], dict)
            ):
                raise SQSExtendedClientException(
                    ExceptionMessages.INVALID_FORMAT_WHEN_RETRIEVING_STORED_S3_MESSAGES
                )
            s3_details = message_body[1]
            s3_bucket_name, s3_key = s3_details["s3BucketName"], s3_details["s3Key"]

            response = self.s3_client.delete_object(Bucket=s3_bucket_name, Key=s3_key)
            # Check if the delete operation succeeded, if not raise an error?
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code != 204:
                raise SQSExtendedClientException(
                    ExceptionMessages.FAILED_DELETE_MESSAGE.format(status_code)
                )
            self.logger.info("Called S3 and deleted the message")

    def _retrieve_message_from_s3(self, message_body: str) -> str:
        """
        Responsible for retrieving a message payload from a S3 Bucket, if it exists
        :message_body: A string containing the first element to be the S3 class pointer
        and the second element to be a dictionary consisting of the s3BucketName and
        the s3Key for the bucket.
        """
        message_body = json.loads(message_body)
        if not (
            isinstance(message_body, list)
            and len(message_body) == 2
            and isinstance(message_body[1], dict)
        ):
            raise SQSExtendedClientException(
                ExceptionMessages.INVALID_FORMAT_WHEN_RETRIEVING_STORED_S3_MESSAGES
            )
        s3_details = message_body[1]
        s3_bucket_name, s3_key = s3_details["s3BucketName"], s3_details["s3Key"]
        response = self.s3_client.get_object(Bucket=s3_bucket_name, Key=s3_key)
        # The message body is under a wrapper class called StreamingBody
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code != 200:
            raise SQSExtendedClientException(
                ExceptionMessages.FAILED_RECEIVE_MESSAGE.format(status_code)
            )
        self.logger.info("Called S3 and received the message")
        streaming_body = response["Body"]
        message_body = streaming_body.read().decode()
        return message_body

    def _store_message_in_s3(
        self, message_body: str, message_attributes: dict, extra_attributes: dict
    ) -> (str, dict):
        """
        Responsible for storing a message payload in a S3 Bucket
        :message_body: A UTF-8 encoded version of the message body
        :message_attributes: A dictionary consisting of message attributes
        :extra_attributes: A dictionary consisting of message attributes
        Each message attribute consists of the name (key) along with a
        type and value of the message body. The following types are supported
        for message attributes: StringValue, BinaryValue and DataType.
        """
        if len(message_body) == 0:
            # Message cannot be empty
            raise SQSExtendedClientException(ExceptionMessages.INVALID_MESSAGE_BODY)

        if self.large_payload_support and self.always_through_s3:
            # Check message attributes for ExtendedClient related constraints
            check_message_attributes(message_attributes)
            encoded_body = message_body.encode("utf-8")

            # Modifying the message attributes for storing it in the Queue
            message_attributes[RESERVED_ATTRIBUTE_NAME] = {}
            attribute_value = {
                "DataType": "Number",
                "StringValue": str(len(encoded_body)),
            }
            message_attributes[RESERVED_ATTRIBUTE_NAME] = attribute_value

            # S3 Key should either be a constant or be a random uuid4 string.
            s3_key = get_s3_key(message_attributes, extra_attributes)

            # Adding the object into the bucket
            response = self.s3_client.put_object(
                Body=encoded_body, Bucket=self.large_payload_support, Key=s3_key
            )
            # Check if the delete operation succeeded, if not raise an error?
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code != 200:
                raise SQSExtendedClientException(
                    ExceptionMessages.FAILED_SUBMIT_MESSAGE.format(status_code)
                )
            self.logger.info(
                f"Message added to S3 bucket [{self.large_payload_support}]"
            )
            # Modifying the message body for storing it in the Queue
            message_body = json.dumps(
                [
                    MESSAGE_POINTER_CLASS,
                    {"s3BucketName": self.large_payload_support, "s3Key": s3_key},
                ]
            )
        return message_body, message_attributes

    def _get_queue_names(self, queues):
        if queues:
            self.logger.info(f"Got queues: {', '.join([q for q in queues])}")
            queue_names = [url.split("/")[-1] for url in queues]
            return queue_names
        self.logger.info("No queues found.")
        return []
