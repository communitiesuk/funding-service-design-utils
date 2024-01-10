import json
from datetime import datetime

import boto3
from botocore.exceptions import ClientError


class SQSClient:
    def __init__(
        self,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        region_name="us-west-1",
        endpoint_url=None,
        **kwargs,
    ):
        if aws_access_key_id and aws_secret_access_key:
            self.client = boto3.client(
                "sqs",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
                endpoint_url=endpoint_url,
                **kwargs,
            )
        else:
            # if 'aws_access_key_id' and 'aws_access_key_id' are not provided make sure to provide
            # 'AWS_ACCESS_KEY_ID' and 'AWS_SECRET_ACCESS_KEY' with environment variables
            self.client = boto3.client(
                "sqs",
                region_name=region_name,
                endpoint_url=endpoint_url,
                **kwargs,
            )

    def get_queues(self, prefix=None):
        """
        Gets a list of SQS queues. When a prefix is specified, only queues with names
        that start with the prefix are returned.

        :param prefix: The prefix used to restrict the list of returned queues.
        :return: A list of Queue names.
        """
        if prefix:
            queues = self.client.list_queues(QueueNamePrefix=prefix)["QueueUrls"]
        else:
            queues = self.client.list_queues()["QueueUrls"]
        if queues:
            print(f"Got queues: {', '.join([q for q in queues])}")
            queue_names = [url.split("/")[-1] for url in queues]
            return queue_names
        else:
            print("No queues found.")
            return []

    def remove_queue(self, queue_url):
        """
        Removes an SQS queue. When run against an AWS account, it can take up to
        60 seconds before the queue is actually deleted.

        :param queue: The queue to delete.
        :return: None
        """
        try:
            self.client.delete_queue(QueueUrl=queue_url)
            print(f"Deleted queue with URL={queue_url}.")
        except ClientError as error:
            print(f"Couldn't delete queue with URL={queue_url}!")
            raise error

    def get_queue_url(self, queue_name):
        """Return queue url for the given queue name."""
        response = self.client.get_queue_url(
            QueueName=queue_name,
        )
        return response["QueueUrl"]

    def submit_single_message(
        self,
        queue_url,
        message,
        extra_attributes: dict = None,
        message_group_id=None,
        message_deduplication_id=None,
    ):
        try:
            SQS_CUSTOM_ATTRIBUTES = {
                "message_created_at": {
                    "StringValue": str(datetime.now()),
                    "DataType": "String",
                },
            }
            # add extra message attributes (if provided)
            if extra_attributes:
                for key, value in extra_attributes.items():
                    SQS_CUSTOM_ATTRIBUTES[key] = value

            print(f"Attempting to place message on queue '{queue_url}'.")

            response = self.client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message),
                MessageAttributes=SQS_CUSTOM_ATTRIBUTES,
                MessageGroupId=message_group_id,
                MessageDeduplicationId=message_deduplication_id,
            )
            message_id = response["MessageId"]
            print(f"Message (id: {message_id}) submitted to queue: {queue_url}.")
            return message_id
        except Exception as e:
            print(
                "Error whilst staging onto queue"
                f" '{queue_url}', message with"
                f" attributes '{str(extra_attributes)}'."
                f" Error : {str(e)}"
            )
            return str(e), 500, {"x-error": "Error"}

    def submit_message(self, queue_url, messages, DelaySeconds=1):
        """
        Send a batch of messages in a single request to an SQS queue.
        This request may return overall success even when some messages were not sent.
        The caller must inspect the Successful and Failed lists in the response and
        resend any failed messages.

        :param queue_url: SQS Queue url.
        :param queue: The queue to receive the messages.
        :param messages: The messages to send to the queue. These are simplified to
                        contain only the message body and attributes.
        :return: The response from SQS that contains the list of successful and failed
                messages.
        """
        try:
            entries = [
                {
                    "Id": str(ind),
                    "MessageBody": msg["body"],
                    "MessageAttributes": msg["attributes"],
                    "DelaySeconds": DelaySeconds,
                }
                for ind, msg in enumerate(messages)
            ]
            response = self.client.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries,
            )
            if "Successful" in response:
                for msg_meta in response["Successful"]:
                    print(
                        f"Message sent to the queue {queue_url}, MessageId: {msg_meta['MessageId']}"
                    )
            if "Failed" in response:
                for msg_meta in response["Failed"]:
                    print(
                        f"Failed to send messages to queue: {queue_url}, "
                        f"attributes {messages[int(msg_meta['Id'])]['attributes']}"
                    )
        except ClientError as error:
            print(f"Send messages failed to queue: {queue_url}")
            raise error
        else:
            return response

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
        try:
            response = self.client.receive_message(
                QueueUrl=queue_url,
                AttributeNames=["SentTimestamp", "ApproximateReceiveCount"],
                MessageAttributeNames=["All"],
                MaxNumberOfMessages=max_number,
                VisibilityTimeout=visibility_time,
                WaitTimeSeconds=wait_time,
            )
            if "Messages" in response.keys():
                messages = response["Messages"]
            elif response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                print(f"No more messages available in queue: {queue_url}")
                return []

            for msg in messages:
                print(
                    f"Received message ID: {msg['MessageId']}, Attributes: {msg['MessageAttributes']}"
                )
        except Exception as error:
            print(f"Couldn't receive messages from queue: {queue_url} Error: {error}")
            raise error
        else:
            return messages

    def delete_messages(self, queue_url, message_receipt_handles):
        """
        Delete a batch of messages from a queue in a single request.

        :param queue_url: SQS Queue url
        :param message_receipt_handles: The list of messages handles to delete.
        :return: The response from SQS that contains the list of successful and failed
                message deletions.
        """
        try:
            entries = [
                {"Id": str(ind), "ReceiptHandle": receipt_handle}
                for ind, receipt_handle in enumerate(message_receipt_handles)
            ]
            response = self.client.delete_message_batch(
                QueueUrl=queue_url, Entries=entries
            )

            if "Successful" in response:
                for msg_meta in response["Successful"]:
                    print(f"Deleted {message_receipt_handles[int(msg_meta['Id'])]}")
            if "Failed" in response:
                for msg_meta in response["Failed"]:
                    print(
                        f"Could not delete {message_receipt_handles[int(msg_meta['Id'])]}"
                    )
        except ClientError:
            print(f"Couldn't delete message from queue {queue_url}")
        else:
            return response

    def create_sqs_queue(
        self, queue_name, has_dlq=False, dlq_queue_name=None, max_recieve_count=3
    ):
        """
        Creates an Amazon SQS & DLQ queue.

        :param queue_name: SQS queue name to create
        :param has_dlq: If true, DLQ(Dead letter queue) is created for given queue
        :param dlq_queue_name: If `has_dlq` is true, then DLQ queue name to create
        :param max_recieve_count: If `has_dlq` is true, then provide the max recieve count
                                  before moving messages to DLQ
        :return: (sqs_queue_url) URL of the queue created.
        """
        # get queue list
        queue_list = self.get_queues()

        # create SQS queue if not exists
        if queue_name not in queue_list:
            sqs_queue_url = self.client.create_queue(
                QueueName=queue_name,
            )["QueueUrl"]
            print(f"Successfully created SQS queue '{queue_name}'")
        else:
            print(f"SQS queue '{queue_name}' already exists!")
            sqs_queue_url = self.client.get_queue_url(QueueName=queue_name)["QueueUrl"]

        if has_dlq:
            # create DLQ queue if not exists
            if dlq_queue_name not in queue_list:
                dlq_queue_url = self.client.create_queue(
                    QueueName=dlq_queue_name,
                )["QueueUrl"]
                dlq_queue_arn = self.client.get_queue_attributes(
                    QueueUrl=dlq_queue_url, AttributeNames=["QueueArn"]
                )["Attributes"]["QueueArn"]
            else:
                print(f"DLQ '{dlq_queue_name}' already exists!")
                dlq_queue_url = self.client.get_queue_url(QueueName=dlq_queue_name)[
                    "QueueUrl"
                ]
                dlq_queue_arn = self.client.get_queue_attributes(
                    QueueUrl=dlq_queue_url, AttributeNames=["QueueArn"]
                )["Attributes"]["QueueArn"]

            redrive_policy = {
                "deadLetterTargetArn": dlq_queue_arn,
                "maxReceiveCount": max_recieve_count,
            }

            self.client.set_queue_attributes(
                QueueUrl=sqs_queue_url,
                Attributes={"RedrivePolicy": json.dumps(redrive_policy)},
            )

        return sqs_queue_url

    def set_queue_attributes(
        self, queue_name: str = None, queue_url: str = None, attributes: dict = {}
    ):
        if not queue_url:
            queue_url = self.client.get_queue_url(QueueName=queue_name)["QueueUrl"]

        self.client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes=attributes,
        )


# Uncomment the below code to test the SQS client usage
# if __name__ == "__main__":

#     sqs_client = SQSClient(
#         aws_access_key_id="FSDIOSFODNN7EXAMPLE",  # pragma: allowlist secret
#         aws_secret_access_key="fsdlrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",  # pragma: allowlist secret
#         region_name="eu-west-2",
#         endpoint_url="http://localhost:4566",
#     )

#     # display all queues
#     print(sqs_client.get_queues())

#     # create my_queue
#     my_queue_url = sqs_client.create_sqs_queue(queue_name="my_queue")
#     print(sqs_client.get_queues())

#     # get queue url
#     print(sqs_client.get_queue_url("my_queue"))

#     # delete my_queue
#     print(sqs_client.remove_queue(my_queue_url))

#     # create my_queue & my_queue_dlq
#     my_queue_url = sqs_client.create_sqs_queue(
#         queue_name="my_queue", has_dlq=True, dlq_queue_name="my_queue_dlq"
#     )
#     print(sqs_client.get_queues())

#     # delete my_queue & my_queue_dlq
#     print(sqs_client.remove_queue(my_queue_url))
#     print(sqs_client.remove_queue(sqs_client.get_queue_url("my_queue_dlq")))
#     print(sqs_client.get_queues())
