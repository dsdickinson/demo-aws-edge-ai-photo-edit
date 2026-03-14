import json
import os
import boto3
import logging
from datetime import datetime

# Environment variables
#TABLE_NAME = os.environ["TABLE_NAME"]
TABLE_NAME = "image-metadata"

# AWS clients
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

# Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate_payload(body):
    required_fields = ["id", "tags"]

    for field in required_fields:
        if field not in body:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(body["tags"], list):
        raise ValueError("Tags must be a list")


def lambda_handler(event, context):
    try:
        logger.info(f"Incoming event: {json.dumps(event)}")

        # API Gateway proxy integration
        body = json.loads(event.get("body", "{}"))

        validate_payload(body)

        item = {
            "id": body["id"],
            "tags": body["tags"],
            "title": body.get("title", ""),
            "description": body.get("description", ""),
            "created_at": datetime.utcnow().isoformat(),
            "request_id": context.aws_request_id
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Metadata stored successfully"})
        }

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
