import unittest
from unittest.mock import MagicMock
from uuid import uuid4

import boto3
from fsd_utils.sqs_scheduler.context_aware_executor import ContextAwareExecutor
from fsd_utils.sqs_scheduler.task_executer_service import TaskExecutorService
from moto import mock_aws


class TestTaskExecutorService(unittest.TestCase):
    @mock_aws
    def test_message_in_mock_environment_processing(self):
        """
        This test ensure that when message is there and if no errors occurred while processing the message
        then successfully removed it from the queue
        """
        self._mock_aws_client()
        self._add_data_to_queue()

        self.task_executor.process_messages()

        self._check_is_data_available(0)

    def _mock_aws_client(self):
        """
        Mocking aws resources and this will act as real aws environment behaviour
        """
        bucket_name = "fsd_msg_s3_bucket"
        self.flask_app = MagicMock()
        self.executor = ContextAwareExecutor(
            max_workers=10, thread_name_prefix="NotifTask", flask_app=self.flask_app
        )
        s3_connection = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id="test_accesstoken",  # pragma: allowlist secret
            aws_secret_access_key="secret_key",  # pragma: allowlist secret
        )
        sqs_connection = boto3.client(
            "sqs",
            region_name="us-east-1",
            aws_access_key_id="test_accesstoken",  # pragma: allowlist secret
            aws_secret_access_key="secret_key",  # pragma: allowlist secret
        )
        s3_connection.create_bucket(Bucket=bucket_name)
        self.queue_response = sqs_connection.create_queue(
            QueueName="notif-queue.fifo", Attributes={"FifoQueue": "true"}
        )
        self.task_executor = AnyTaskExecutorService(
            flask_app=MagicMock(),
            executor=self.executor,
            s3_bucket=bucket_name,
            sqs_primary_url=self.queue_response["QueueUrl"],
            task_executor_max_thread=5,
            sqs_batch_size=10,
            visibility_time=1,
            sqs_wait_time=2,
            endpoint_url_override=None,
            aws_access_key_id="test_accesstoken",  # pragma: allowlist secret
            aws_secret_access_key="secret_key",  # pragma: allowlist secret
            region_name="us-east-1",
        )
        self.task_executor.sqs_extended_client.sqs_client = sqs_connection
        self.task_executor.sqs_extended_client.s3_client = s3_connection

    def _add_data_to_queue(self):
        """
        Adding test data into the queue
        """
        for x in range(1):
            message_id = self.task_executor.sqs_extended_client.submit_single_message(
                queue_url=self.queue_response["QueueUrl"],
                message="message",
                message_group_id="import_applications_group",
                message_deduplication_id=str(uuid4()),  # ensures message uniqueness
            )
            assert message_id is not None

    def _check_is_data_available(self, count):
        response = self.task_executor.sqs_extended_client.receive_messages(
            queue_url=self.queue_response["QueueUrl"], max_number=1
        )
        assert len(response) == count


class AnyTaskExecutorService(TaskExecutorService):
    def message_executor(self, message):
        return message
