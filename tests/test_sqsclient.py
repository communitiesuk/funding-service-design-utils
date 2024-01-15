import json
import unittest
from datetime import datetime
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

from fsd_utils.services.aws import SQSClient


class TestSQSClient(unittest.TestCase):
    def setUp(self):
        # Create a mock Boto3 SQS client for testing
        self.sqs_client = MagicMock()
        self.sqs_client.list_queues.return_value = {"QueueUrls": ["url1", "url2"]}
        self.sqs_client.delete_queue.return_value = {}

        # Create an instance of SQSClient with the mock client
        self.sqs = SQSClient("your_access_key", "your_secret_key")
        self.sqs.client = self.sqs_client

    def test_get_queues(self):
        # Test the get_queues method without a prefix
        queue_names = self.sqs.get_queues()
        self.assertEqual(queue_names, ["url1", "url2"])

    def test_remove_queue_success(self):
        # Test the remove_queue method when the queue is successfully deleted
        queue_url = "test_queue_url"
        self.sqs.remove_queue(queue_url)
        self.sqs_client.delete_queue.assert_called_with(QueueUrl=queue_url)

    def test_remove_queue_failure(self):
        # Test the remove_queue method when there is an error
        queue_url = "test_queue_url"
        self.sqs_client.delete_queue.side_effect = Exception("Queue deletion failed")
        with self.assertRaises(Exception):
            self.sqs.remove_queue(queue_url)

    def test_get_queue_url(self):
        # Mock data & responses
        queue_name = "test_queue"
        expected_queue_url = (
            "https://sqs.us-west-1.amazonaws.com/123456789012/test_queue"
        )
        self.sqs_client.get_queue_url.return_value = {"QueueUrl": expected_queue_url}

        # call to the function
        actual_queue_url = self.sqs.get_queue_url(queue_name)

        # Assert responses
        self.assertEqual(actual_queue_url, expected_queue_url)
        self.sqs_client.get_queue_url.assert_called_with(QueueName=queue_name)

    def test_submit_single_message(self):
        # Mock data & responses
        queue_url = "https://sqs.us-west-1.amazonaws.com/123456789012/test_queue"
        message = {"key": "value"}
        message_group_id = "group_id"
        message_deduplication_id = "deduplication_id"
        expected_message_id = "test_message_id"

        self.sqs_client.send_message.return_value = {"MessageId": expected_message_id}

        with patch("fsd_utils.services.aws.datetime") as mock_datetime:
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
                MessageBody=json.dumps(message),
                MessageAttributes={
                    "message_created_at": {
                        "StringValue": str(datetime_now),
                        "DataType": "String",
                    }
                },
                MessageGroupId=message_group_id,
                MessageDeduplicationId=message_deduplication_id,
            )

    def test_submit_message(self):
        # Mock data & responses
        queue_url = "http://localhost:4576/queue/test_queue"
        messages = [
            {"body": {"key1": "value1"}, "attributes": {"attr1": "attr_value1"}},
            {"body": {"key2": "value2"}, "attributes": {"attr2": "attr_value2"}},
            {"body": {"key3": "value3"}, "attributes": {"attr3": "attr_value3"}},
            {"body": {"key4": "value4"}, "attributes": {"attr4": "attr_value4"}},
        ]
        expected_response = {
            "Successful": [{"MessageId": "msg1"}, {"MessageId": "msg2"}],
            "Failed": [{"Id": "2"}, {"Id": "3"}],
        }
        self.sqs_client.send_message_batch.return_value = expected_response

        # call to the function
        actual_response = self.sqs.submit_message(queue_url, messages, DelaySeconds=1)

        # Assert responses
        self.assertEqual(actual_response, expected_response)

    def test_receive_messages(self):
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
        response = {"Messages": messages}
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

    def test_delete_messages(self):
        # Mock data & responses
        queue_url = "http://localhost:4576/queue/test_queue"
        message_receipt_handles = [
            "receipt_handle1",
            "receipt_handle2",
            "receipt_handle3",
        ]
        response = {
            "Successful": [{"Id": "0"}, {"Id": "1"}],
            "Failed": [{"Id": "2"}],
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

    def test_create_sqs_queue(self):
        # Mock data & responses
        queue_name = "test_queue"
        has_dlq = True
        dlq_queue_name = "test_dlq"
        dlq_arn = "arn:aws:sqs:us-west-1:123456789012:test_dlq"
        max_receive_count = 3
        queue_url = "http://localhost:4576/queue/test_queue"
        dlq_queue_url = "http://localhost:4576/queue/test_dlq"
        self.sqs_client.get_queues.return_value = ["existing_queue"]
        self.sqs_client.create_queue.side_effect = [
            {"QueueUrl": queue_url},
            {"QueueUrl": dlq_queue_url},
        ]
        self.sqs_client.get_queue_url.return_value = {"QueueUrl": queue_url}
        self.sqs_client.get_queue_attributes.return_value = {
            "Attributes": {"QueueArn": dlq_arn}
        }

        # call to the function
        sqs_queue_url = self.sqs.create_sqs_queue(
            queue_name, has_dlq, dlq_queue_name, max_receive_count
        )

        # Assert responses
        self.assertEqual(sqs_queue_url, queue_url)
        self.sqs_client.create_queue.assert_has_calls(
            [
                call(QueueName=queue_name),
                call(QueueName=dlq_queue_name),
            ],
            any_order=True,
        )
        expected_redrive_policy = {
            "deadLetterTargetArn": dlq_arn,
            "maxReceiveCount": max_receive_count,
        }
        self.sqs_client.set_queue_attributes.assert_called_with(
            QueueUrl=queue_url,
            Attributes={"RedrivePolicy": json.dumps(expected_redrive_policy)},
        )

    def test_set_queue_attributes_with_queue_name(self):
        # Mock data & responses
        queue_name = "test_queue"
        queue_url = "http://localhost:4576/queue/test_queue"
        attributes = {"VisibilityTimeout": "10", "MaximumMessageSize": "1024"}
        self.sqs_client.get_queue_url.return_value = {"QueueUrl": queue_url}

        # call to the function
        self.sqs.set_queue_attributes(queue_name=queue_name, attributes=attributes)

        # Assert responses
        self.sqs_client.set_queue_attributes.assert_called_with(
            QueueUrl=queue_url,
            Attributes=attributes,
        )

    def test_set_queue_attributes_with_queue_url(self):
        # Mock data & responses
        queue_url = "http://localhost:4576/queue/test_queue"
        attributes = {"VisibilityTimeout": "10", "MaximumMessageSize": "1024"}

        # call to the function
        self.sqs.set_queue_attributes(queue_url=queue_url, attributes=attributes)

        # Assert responses
        self.sqs_client.set_queue_attributes.assert_called_with(
            QueueUrl=queue_url,
            Attributes=attributes,
        )
