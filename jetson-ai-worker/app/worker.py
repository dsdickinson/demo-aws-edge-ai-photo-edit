import boto3
import requests
import logging
import os
import time
import json
import uuid6

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
       body = json.loads(message["Body"])

       if body.get("Event") == "s3:TestEvent":
          logger.info("Ignoring S3 test event")
       else:
          record = body["Records"][0]
          bucket = record["s3"]["bucket"]["name"]
          key = record["s3"]["object"]["key"]
          image_id = uuid6.uuid7()
          image_name = key.split("/")[-1]

          #bucket = self.config["aws"]["s3"]["bucket_name"]
          download_dir = self.config["aws"]["s3"]["download_dir"]
          local_path = os.path.join(download_dir, os.path.basename(image_name))
  
          logger.info(f"Downloading {bucket} {image_name} {local_path}")
          self.s3.download_file(bucket, image_name, local_path)
  
          tags = self.inference.run(local_path)
          title = f"{tags[0].title()}"
          description = f"A fine art wildlife photograph featuring {', '.join(tags)}."
 #         inference_time = "XXX"
 #         gpu_available = "XXX"
 #         status = "XXX"
  
          metadata = {
              "id": image_id,
              "name": image_name,
              "title": title,
              "description": description,
              "tags": tags
          }

          # Do this to serialize the uuid
          metadata_str = json.dumps(metadata, default=lambda x: str(x))
  
          api_endpoint = self.config["aws"]["api"]["endpoint"]
  
          logger.info(f"Posting metadata for {image_name}")
          response = requests.post(api_endpoint, json=metadata_str)
          response.raise_for_status()
  
          self.sqs.delete_message(
              QueueUrl=self.config["aws"]["sqs"]["queue_url"],
              ReceiptHandle=message["ReceiptHandle"]
          )
  
          logger.info(f"Successfully processed {image_name}")

    def run(self):
        queue_url = self.config["aws"]["sqs"]["queue_url"]

        while True:
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=self.config["aws"]["sqs"]["max_messages"],
                WaitTimeSeconds=self.config["aws"]["sqs"]["wait_time_seconds"]
            )

            logger.info(f"SQS response: {response}")

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
