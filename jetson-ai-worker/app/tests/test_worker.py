import pytest
from worker import JetsonWorker

class DummyInference:
    def run(self, path):
        return ["heron"]

def test_process_message_success(mocker):
    config = {
        "aws": {
            "region": "us-east-1",
            "s3": {
                "bucket_name": "bucket",
                "download_dir": "/tmp"
            },
            "sqs": {
                "queue_url": "queue-url"
            },
            "api": {
                "endpoint": "http://api"
            }
        }
    }

    inference = DummyInference()
    worker = JetsonWorker(config, inference)

    # Mock AWS clients
    mock_s3 = mocker.patch.object(worker, "s3")
    mock_sqs = mocker.patch.object(worker, "sqs")
    mock_post = mocker.patch("worker.requests.post")

    mock_post.return_value.raise_for_status.return_value = None

    message = {
        "Body": "image.jpg",
        "ReceiptHandle": "abc"
    }

    worker.process_message(message)

    mock_s3.download_file.assert_called_once()
    mock_post.assert_called_once()
    mock_sqs.delete_message.assert_called_once()
