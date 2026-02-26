import boto3
import requests
import logging
import os
import time

logger = logging.getLogger("worker")

class JetsonWorker:
    def __init__(self, config, inference_engine):
        self.config = config
        self.inference = inference_engine

        self.sqs = boto3.client(
            "sqs",
            region_name=config["aws"]["region"]
        )

        self.s3 = boto3.client(
            "s3",
            region_name=config["aws"]["region"]
        )

    def process_message(self, message):
        image_key = message["Body"]
        bucket = self.config["aws"]["s3"]["bucket_name"]
        download_dir = self.config["aws"]["s3"]["download_dir"]
        local_path = os.path.join(download_dir, os.path.basename(image_key))

        logger.info(f"Downloading {image_key}")
        self.s3.download_file(bucket, image_key, local_path)

        tags = self.inference.run(local_path)
        title = f"{tags[0].title()}"
        description = f"A fine art wildlife photograph featuring {', '.join(tags)}."

        metadata = {
            "image_id": image_key,
            "title": title,
            "description": description,
            "tags": tags
            "inference_time_ms": inference_time,
            "gpu": gpu_available,
            "status": status
        }

        api_endpoint = self.config["aws"]["api"]["endpoint"]

        logger.info(f"Posting metadata for {image_key}")
        response = requests.post(api_endpoint, json=metadata)
        response.raise_for_status()

        self.sqs.delete_message(
            QueueUrl=self.config["aws"]["sqs"]["queue_url"],
            ReceiptHandle=message["ReceiptHandle"]
        )

        logger.info(f"Successfully processed {image_key}")

    def run(self):
        queue_url = self.config["aws"]["sqs"]["queue_url"]

        while True:
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=self.config["aws"]["sqs"]["max_messages"],
                WaitTimeSeconds=self.config["aws"]["sqs"]["wait_time_seconds"]
            )

            messages = response.get("Messages", [])

            if not messages:
                logger.debug("No messages received")
                continue

            for message in messages:
                try:
                    self.process_message(message)
                except Exception as e:
                    logger.error(f"Processing failed: {e}", exc_info=True)

            time.sleep(1)
