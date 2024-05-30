import json
import unittest
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

import pytest
from fsd_utils.services.aws_extended_client import SQSExtendedClient
from fsd_utils.services.aws_sqs_extended_client_exception import (
    SQSExtendedClientException,
)


class TestSQSExtendedClient(unittest.TestCase):
    def setUp(self):
        # Create a mock Boto3 SQS client for testing without extended client behaviour
        self.sqs_client = MagicMock()
        self.sqs_client.list_queues.return_value = {"QueueUrls": ["url1", "url2"]}
        self.sqs_client.delete_queue.return_value = {}
        # Create an instance of SQSClient with the mock client
        self.sqs = SQSExtendedClient(
            aws_access_key_id="your_access_key",  # pragma: allowlist secret
            aws_secret_access_key="your_secret_key",  # pragma: allowlist secret
            logger=MagicMock(),
        )
        self.sqs.sqs_client = self.sqs_client

        # Create a mock Boto3 SQS client for testing with extended client behaviour
        self.s3_client = MagicMock()
        self.sqs_client.list_queues.return_value = {"QueueUrls": ["url1", "url2"]}
        self.sqs_client.delete_queue.return_value = {}
        # Create an instance of SQSClient with the mock client
        self.sqs_extended = SQSExtendedClient(
            aws_access_key_id="your_access_key",  # pragma: allowlist secret
            aws_secret_access_key="your_secret_key",  # pragma: allowlist secret
            large_payload_support="fsd_sqs_extended_helper",
            always_through_s3=True,
            delete_payload_from_s3=True,
            logger=MagicMock(),
        )
        self.sqs_extended.sqs_client = self.sqs_client
        self.sqs_extended.s3_client = self.s3_client

    def test_get_queues_without_extended_client_behaviour(self):
        # Test the get_queues method without a prefix
        queue_names = self.sqs.get_queues()
        self.assertEqual(queue_names, ["url1", "url2"])

    def test_get_queues_with_extended_client_behaviour(self):
        # Test the get_queues method without a prefix
        queue_names = self.sqs_extended.get_queues()
        self.assertEqual(queue_names, ["url1", "url2"])

    def test_submit_single_message_without_extended_client_behaviour(self):
        # Mock data & responses
        queue_url = "https://sqs.us-west-1.amazonaws.com/123456789012/test_queue"
        message = "{'key': 'value'}"
        message_group_id = "group_id"
        message_deduplication_id = "deduplication_id"
        expected_message_id = "test_message_id"

        self.sqs_client.send_message.return_value = {
            "MessageId": expected_message_id,
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }

        with patch("fsd_utils.services.aws_extended_client.datetime") as mock_datetime:
            datetime_now = datetime(2023, 1, 1, 12, 0, 0)
            mock_datetime.now.return_value = datetime_now

            # call to the function
            actual_message_id = self.sqs.submit_single_message(
                queue_url,
                message,
                message_group_id=message_group_id,
                message_deduplication_id=message_deduplication_id,
            )

            # Assert responses
            self.assertEqual(actual_message_id, expected_message_id)
            self.sqs_client.send_message.assert_called_with(
                QueueUrl=queue_url,
                MessageBody=message,
                MessageAttributes={
                    "message_created_at": {
                        "StringValue": str(datetime_now),
                        "DataType": "String",
                    }
                },
                MessageGroupId=message_group_id,
                MessageDeduplicationId=message_deduplication_id,
            )

    def test_submit_single_message_with_extended_client_behaviour(self):
        # Mock data & responses
        queue_url = "https://sqs.us-west-1.amazonaws.com/123456789012/test_queue"
        message = "{'key': 'value'}"
        message_group_id = "group_id"
        message_deduplication_id = "deduplication_id"
        expected_message_id = "test_message_id"

        self.sqs_client.send_message.return_value = {
            "MessageId": expected_message_id,
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }

        self.s3_client.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

        with patch("fsd_utils.services.aws_extended_client.datetime") as mock_datetime:
            with patch(
                "fsd_utils.services.aws_sqs_extended_client_util.uuid4"
            ) as mock_uuid:
                uuid_val = uuid4()
                datetime_now = datetime(2023, 1, 1, 12, 0, 0)
                mock_datetime.now.return_value = datetime_now
                mock_uuid.return_value = uuid_val

                message_body = json.dumps(
                    [
                        "software.amazon.payloadoffloading.PayloadS3Pointer",
                        {
                            "s3BucketName": "fsd_sqs_extended_helper",
                            "s3Key": str(uuid_val),
                        },
                    ]
                )

                # call to the function
                actual_message_id = self.sqs_extended.submit_single_message(
                    queue_url,
                    message,
                    message_group_id=message_group_id,
                    message_deduplication_id=message_deduplication_id,
                )

                # Assert responses
                self.assertEqual(actual_message_id, expected_message_id)
                self.sqs_client.send_message.assert_called_with(
                    QueueUrl=queue_url,
                    MessageBody=message_body,
                    MessageAttributes={
                        "ExtendedPayloadSize": {
                            "DataType": "Number",
                            "StringValue": "16",
                        },
                        "message_created_at": {
                            "StringValue": str(datetime_now),
                            "DataType": "String",
                        },
                    },
                    MessageGroupId=message_group_id,
                    MessageDeduplicationId=message_deduplication_id,
                )

    def test_submit_single_message_with_extended_client_behaviour_with_s3key(self):
        # Mock data & responses
        queue_url = "https://sqs.us-west-1.amazonaws.com/123456789012/test_queue"
        message = "{'key': 'value'}"
        message_group_id = "group_id"
        message_deduplication_id = "deduplication_id"
        expected_message_id = "test_message_id"

        self.sqs_client.send_message.return_value = {
            "MessageId": expected_message_id,
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }

        self.s3_client.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

        with patch("fsd_utils.services.aws_extended_client.datetime") as mock_datetime:
            with patch(
                "fsd_utils.services.aws_sqs_extended_client_util.uuid4"
            ) as mock_uuid:
                uuid_val = uuid4()
                datetime_now = datetime(2023, 1, 1, 12, 0, 0)
                mock_datetime.now.return_value = datetime_now
                mock_uuid.return_value = uuid_val

                message_body = json.dumps(
                    [
                        "software.amazon.payloadoffloading.PayloadS3Pointer",
                        {
                            "s3BucketName": "fsd_sqs_extended_helper",
                            "s3Key": "notification/" + str(uuid_val),
                        },
                    ]
                )

                # call to the function
                actual_message_id = self.sqs_extended.submit_single_message(
                    queue_url,
                    message,
                    message_group_id=message_group_id,
                    message_deduplication_id=message_deduplication_id,
                    extra_attributes={
                        "S3Key": {
                            "StringValue": "notification",
                            "DataType": "String",
                        },
                    },
                )

                # Assert responses
                self.assertEqual(actual_message_id, expected_message_id)
                self.sqs_client.send_message.assert_called_with(
                    QueueUrl=queue_url,
                    MessageBody=message_body,
                    MessageAttributes={
                        "ExtendedPayloadSize": {
                            "DataType": "Number",
                            "StringValue": "16",
                        },
                        "S3Key": {"DataType": "String", "StringValue": "notification"},
                        "message_created_at": {
                            "StringValue": str(datetime_now),
                            "DataType": "String",
                        },
                    },
                    MessageGroupId=message_group_id,
                    MessageDeduplicationId=message_deduplication_id,
                )

    def test_submit_single_message_with_extended_client_behaviour_error_sqs(self):
        # Mock data & responses
        queue_url = "https://sqs.us-west-1.amazonaws.com/123456789012/test_queue"
        message = "{'key': 'value'}"
        message_group_id = "group_id"
        message_deduplication_id = "deduplication_id"
        expected_message_id = "test_message_id"

        self.sqs_client.send_message.return_value = {
            "MessageId": expected_message_id,
            "ResponseMetadata": {"HTTPStatusCode": 500},
        }

        self.s3_client.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

        with patch("fsd_utils.services.aws_extended_client.datetime") as mock_datetime:
            with patch(
                "fsd_utils.services.aws_sqs_extended_client_util.uuid4"
            ) as mock_uuid:
                uuid_val = uuid4()
                datetime_now = datetime(2023, 1, 1, 12, 0, 0)
                mock_datetime.now.return_value = datetime_now
                mock_uuid.return_value = uuid_val

                with pytest.raises(
                    SQSExtendedClientException,
                    match="submit_single_message failed with status code 500",
                ):
                    # call to the function
                    self.sqs_extended.submit_single_message(
                        queue_url,
                        message,
                        message_group_id=message_group_id,
                        message_deduplication_id=message_deduplication_id,
                    )

    def test_submit_single_message_with_extended_client_behaviour_error_s3(self):
        # Mock data & responses
        queue_url = "https://sqs.us-west-1.amazonaws.com/123456789012/test_queue"
        message = "{'key': 'value'}"
        message_group_id = "group_id"
        message_deduplication_id = "deduplication_id"
        expected_message_id = "test_message_id"

        self.sqs_client.send_message.return_value = {
            "MessageId": expected_message_id,
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }

        self.s3_client.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 500}
        }

        with pytest.raises(
            SQSExtendedClientException,
            match="submit_single_message failed with status code 500",
        ):
            # call to the function
            self.sqs_extended.submit_single_message(
                queue_url,
                message,
                message_group_id=message_group_id,
                message_deduplication_id=message_deduplication_id,
            )

    def test_receive_messages_without_extended_client_behaviour(self):
        # Mock data & responses
        queue_url = "http://localhost:4576/queue/test_queue"
        max_number = 5
        visibility_time = 10
        wait_time = 2
        messages = [
            {
                "MessageId": "msg1",
                "MessageAttributes": {"attr1": "value1"},
                "MessageBody": "Message 1",
            },
            {
                "MessageId": "msg2",
                "MessageAttributes": {"attr2": "value2"},
                "MessageBody": "Message 2",
            },
        ]
        response = {"Messages": messages, "ResponseMetadata": {"HTTPStatusCode": 200}}
        self.sqs_client.receive_message.return_value = response

        # call to the function
        received_messages = self.sqs.receive_messages(
            queue_url, max_number, visibility_time, wait_time
        )

        # Assert responses
        self.assertEqual(received_messages, messages)
        self.sqs_client.receive_message.assert_called_with(
            QueueUrl=queue_url,
            AttributeNames=["SentTimestamp", "ApproximateReceiveCount"],
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_number,
            VisibilityTimeout=visibility_time,
            WaitTimeSeconds=wait_time,
        )

    def test_receive_messages_with_extended_client_behaviour(self):
        # Mock data & responses
        uuid_val = uuid4()
        queue_url = "http://localhost:4576/queue/test_queue"
        max_number = 5
        visibility_time = 10
        wait_time = 2
        message_body = json.dumps(
            [
                "software.amazon.payloadoffloading.PayloadS3Pointer",
                {"s3BucketName": "fsd_sqs_extended_helper", "s3Key": str(uuid_val)},
            ]
        )
        messages = [
            {
                "MessageId": "msg1",
                "MessageAttributes": {"attr1": "value1"},
                "Body": message_body,
            }
        ]
        response = {"Messages": messages, "ResponseMetadata": {"HTTPStatusCode": 200}}
        body_data = MagicMock()
        body_data.read.decode = "Testing"
        s3_response = {"Body": body_data, "ResponseMetadata": {"HTTPStatusCode": 200}}
        s3_response["Body"].read.decode = "Testing"
        self.sqs_client.receive_message.return_value = response
        self.s3_client.get_object.return_value = s3_response

        # call to the function
        received_messages = self.sqs_extended.receive_messages(
            queue_url, max_number, visibility_time, wait_time
        )

        # Assert responses
        self.assertEqual(received_messages[0]["sqs"], messages[0])
        self.sqs_client.receive_message.assert_called_with(
            QueueUrl=queue_url,
            AttributeNames=["SentTimestamp", "ApproximateReceiveCount"],
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_number,
            VisibilityTimeout=visibility_time,
            WaitTimeSeconds=wait_time,
        )

    def test_receive_messages_with_extended_client_behaviour_error_sqs(self):
        # Mock data & responses
        uuid_val = uuid4()
        queue_url = "http://localhost:4576/queue/test_queue"
        max_number = 5
        visibility_time = 10
        wait_time = 2
        message_body = json.dumps(
            [
                "software.amazon.payloadoffloading.PayloadS3Pointer",
                {"s3BucketName": "fsd_sqs_extended_helper", "s3Key": str(uuid_val)},
            ]
        )
        messages = [
            {
                "MessageId": "msg1",
                "MessageAttributes": {"attr1": "value1"},
                "Body": message_body,
            }
        ]
        response = {"Messages": messages, "ResponseMetadata": {"HTTPStatusCode": 500}}
        body_data = MagicMock()
        body_data.read.decode = "Testing"
        s3_response = {"Body": body_data, "ResponseMetadata": {"HTTPStatusCode": 200}}
        s3_response["Body"].read.decode = "Testing"
        self.sqs_client.receive_message.return_value = response
        self.s3_client.get_object.return_value = s3_response

        # call to the function
        with pytest.raises(
            SQSExtendedClientException,
            match="receive_messages failed with status code 500",
        ):
            self.sqs_extended.receive_messages(
                queue_url, max_number, visibility_time, wait_time
            )

    def test_receive_messages_with_extended_client_behaviour_error_s3(self):
        # Mock data & responses
        uuid_val = uuid4()
        queue_url = "http://localhost:4576/queue/test_queue"
        max_number = 5
        visibility_time = 10
        wait_time = 2
        message_body = json.dumps(
            [
                "software.amazon.payloadoffloading.PayloadS3Pointer",
                {"s3BucketName": "fsd_sqs_extended_helper", "s3Key": str(uuid_val)},
            ]
        )
        messages = [
            {
                "MessageId": "msg1",
                "MessageAttributes": {"attr1": "value1"},
                "Body": message_body,
            }
        ]
        response = {"Messages": messages, "ResponseMetadata": {"HTTPStatusCode": 200}}
        s3_response = {"Body": "eee", "ResponseMetadata": {"HTTPStatusCode": 500}}
        self.sqs_client.receive_message.return_value = response
        self.s3_client.get_object.return_value = s3_response

        # call to the function
        with pytest.raises(
            SQSExtendedClientException,
            match="receive_messages failed with status code 500",
        ):
            self.sqs_extended.receive_messages(
                queue_url, max_number, visibility_time, wait_time
            )

    def test_delete_messages_without_extended_client_behaviour(self):
        # Mock data & responses
        queue_url = "http://localhost:4576/queue/test_queue"
        message_receipt_handles = [
            {
                "MessageId": "msg_id_1",
                "ReceiptHandle": "receipt_handle1",
                "Body": "body 1",
            },
            {
                "MessageId": "msg_id_2",
                "ReceiptHandle": "receipt_handle2",
                "Body": "body 2",
            },
            {
                "MessageId": "msg_id_3",
                "ReceiptHandle": "receipt_handle3",
                "Body": "body 3",
            },
        ]
        response = {
            "Successful": [{"Id": "0"}, {"Id": "1"}],
            "Failed": [{"Id": "2"}],
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }
        self.sqs_client.delete_message_batch.return_value = response

        # call to the function
        deleted_response = self.sqs.delete_messages(queue_url, message_receipt_handles)

        # Assert responses
        self.assertEqual(deleted_response, response)
        expected_entries = [
            {"Id": "0", "ReceiptHandle": "receipt_handle1"},
            {"Id": "1", "ReceiptHandle": "receipt_handle2"},
            {"Id": "2", "ReceiptHandle": "receipt_handle3"},
        ]
        self.sqs_client.delete_message_batch.assert_called_with(
            QueueUrl=queue_url, Entries=expected_entries
        )

    def test_delete_messages_with_extended_client_behaviour(self):
        uuid_val = uuid4()
        # Mock data & responses
        queue_url = "http://localhost:4576/queue/test_queue"
        message_body = json.dumps(
            [
                "software.amazon.payloadoffloading.PayloadS3Pointer",
                {"s3BucketName": "fsd_sqs_extended_helper", "s3Key": str(uuid_val)},
            ]
        )
        message_receipt_handles = [
            {
                "MessageId": "msg_id_1",
                "ReceiptHandle": "receipt_handle1",
                "Body": message_body,
            }
        ]
        response = {
            "Successful": [{"Id": "0"}],
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }
        s3_response = {"ResponseMetadata": {"HTTPStatusCode": 204}}
        self.s3_client.delete_object.return_value = s3_response
        self.sqs_client.delete_message_batch.return_value = response

        # call to the function
        deleted_response = self.sqs_extended.delete_messages(
            queue_url, message_receipt_handles
        )

        # Assert responses
        self.assertEqual(deleted_response, response)
        expected_entries = [{"Id": "0", "ReceiptHandle": "receipt_handle1"}]
        self.sqs_client.delete_message_batch.assert_called_with(
            QueueUrl=queue_url, Entries=expected_entries
        )

    def test_delete_messages_with_extended_client_behaviour_error_sqs(self):
        uuid_val = uuid4()
        # Mock data & responses
        queue_url = "http://localhost:4576/queue/test_queue"
        message_body = json.dumps(
            [
                "software.amazon.payloadoffloading.PayloadS3Pointer",
                {"s3BucketName": "fsd_sqs_extended_helper", "s3Key": str(uuid_val)},
            ]
        )
        message_receipt_handles = [
            {
                "MessageId": "msg_id_1",
                "ReceiptHandle": "receipt_handle1",
                "Body": message_body,
            }
        ]
        response = {
            "Successful": [{"Id": "0"}],
            "ResponseMetadata": {"HTTPStatusCode": 500},
        }
        s3_response = {"ResponseMetadata": {"HTTPStatusCode": 204}}
        self.s3_client.delete_object.return_value = s3_response
        self.sqs_client.delete_message_batch.return_value = response

        # call to the function
        with pytest.raises(
            SQSExtendedClientException,
            match="delete_object failed with status code 500",
        ):
            self.sqs_extended.delete_messages(queue_url, message_receipt_handles)

    def test_delete_messages_with_extended_client_behaviour_error_s3(self):
        uuid_val = uuid4()
        # Mock data & responses
        queue_url = "http://localhost:4576/queue/test_queue"
        message_body = json.dumps(
            [
                "software.amazon.payloadoffloading.PayloadS3Pointer",
                {"s3BucketName": "fsd_sqs_extended_helper", "s3Key": str(uuid_val)},
            ]
        )
        message_receipt_handles = [
            {
                "MessageId": "msg_id_1",
                "ReceiptHandle": "receipt_handle1",
                "Body": message_body,
            }
        ]
        response = {
            "Successful": [{"Id": "0"}],
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }
        s3_response = {"ResponseMetadata": {"HTTPStatusCode": 500}}
        self.s3_client.delete_object.return_value = s3_response
        self.sqs_client.delete_message_batch.return_value = response

        # call to the function
        with pytest.raises(
            SQSExtendedClientException,
            match="delete_object failed with status code 500",
        ):
            self.sqs_extended.delete_messages(queue_url, message_receipt_handles)
