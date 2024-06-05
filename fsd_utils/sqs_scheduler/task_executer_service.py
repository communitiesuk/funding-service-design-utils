import threading
from abc import abstractmethod
from concurrent.futures import as_completed

from fsd_utils.services.aws_extended_client import SQSExtendedClient


class TaskExecutorService:
    def __init__(
        self,
        flask_app,
        executor,
        s3_bucket,
        sqs_primary_url,
        task_executor_max_thread,
        sqs_batch_size,
        visibility_time,
        sqs_wait_time,
        endpoint_url_override=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        region_name=None,
    ):
        self.executor = executor
        self.sqs_primary_url = sqs_primary_url
        self.task_executor_max_thread = task_executor_max_thread
        self.sqs_batch_size = sqs_batch_size
        self.visibility_time = visibility_time
        self.sqs_wait_time = sqs_wait_time
        self.logger = flask_app.logger
        self.sqs_extended_client = SQSExtendedClient(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            endpoint_url=endpoint_url_override,
            large_payload_support=s3_bucket,
            always_through_s3=True,
            delete_payload_from_s3=True,
            logger=self.logger,
        )
        self.logger.info(
            "Created the thread pool executor to process messages in extended SQS queue"
        )

    def process_messages(self):
        """
        Scheduler calling this method based on a cron job for every given second then messages will be read
        from the SQS queue in AWS and if S3 usage is allowed then it will interact each other to retrieve the messages
        """
        current_thread = threading.current_thread()
        thread_id = f"[{current_thread.name}:{current_thread.ident}]"
        self.logger.debug(f"{thread_id} Triggered schedular to get messages")

        running_threads, read_msg_ids = self._handle_message_receiving_and_processing()

        self._handle_message_delete_processing(running_threads, read_msg_ids)

        self.logger.debug(
            f"{thread_id} Message Processing completed and will start again later"
        )

    @abstractmethod
    def message_executor(self, message):
        """
        Processing the message in a separate worker thread and this will call the GOV notify service to send emails
        :param message Json message
        override this for implementation
        """
        pass

    def _handle_message_receiving_and_processing(self):
        """
        Handle message retrieve from the SQS service and get the json from S3 bucket
        """
        current_thread = threading.current_thread()
        thread_id = f"[{current_thread.name}:{current_thread.ident}]"
        running_threads = []
        read_msg_ids = []
        if self.task_executor_max_thread >= self.executor.queue_size():
            sqs_messages = self.sqs_extended_client.receive_messages(
                self.sqs_primary_url,
                self.sqs_batch_size,
                self.visibility_time,
                self.sqs_wait_time,
            )
            self.logger.debug(f"{thread_id} Message Count [{len(sqs_messages)}]")
            if sqs_messages:
                for message in sqs_messages:
                    message_id = message["sqs"]["MessageId"]
                    self.logger.info(f"{thread_id} Message id [{message_id}]")
                    read_msg_ids.append(message["sqs"]["MessageId"])
                    task = self.executor.submit(self.message_executor, message)
                    running_threads.append(task)
        else:
            self.logger.info(
                f"{thread_id} Max thread limit reached hence stop reading messages from queue"
            )

        self.logger.debug(
            f"{thread_id} Received Message count [{len(read_msg_ids)}] "
            f"Created thread count [{len(running_threads)}]"
        )
        return running_threads, read_msg_ids

    def _handle_message_delete_processing(self, running_threads, read_msg_ids):
        """
        Handling the message delete process from the SQS and S3 bucket if it is completed
        :param read_msg_ids All the message ids that taken from SQS
        :param running_threads Executing tasks to send emails
        """
        current_thread = threading.current_thread()
        thread_id = f"[{current_thread.name}:{current_thread.ident}]"
        receipt_handles_to_delete = []
        completed_msg_ids = []
        for future in as_completed(running_threads):
            try:
                msg = future.result()
                msg_id = msg["sqs"]["MessageId"]
                receipt_handles_to_delete.append(msg["sqs"])
                completed_msg_ids.append(msg_id)
                self.logger.debug(
                    f"{thread_id} Execution completed and deleted from queue: {msg_id}"
                )
            except Exception as e:
                self.logger.error(
                    f"{thread_id} An error occurred while processing the message {e}"
                )
        dif_msg_ids = [i for i in read_msg_ids if i not in completed_msg_ids]
        self.logger.debug(
            f"No of messages not processed [{len(dif_msg_ids)}] and msg ids are {dif_msg_ids}"
        )
        if receipt_handles_to_delete:
            self.sqs_extended_client.delete_messages(
                self.sqs_primary_url, receipt_handles_to_delete
            )
