import json
import pytest
from unittest.mock import patch, MagicMock
from handler import lambda_handler


class DummyContext:
    aws_request_id = "test-request-id"


@patch("handler.table")
def test_lambda_success(mock_table):
    mock_table.put_item.return_value = {}

    event = {
        "body": json.dumps({
            "image_id": "img123.jpg",
            "tags": ["heron"]
        })
    }

    response = lambda_handler(event, DummyContext())

    assert response["statusCode"] == 200
    mock_table.put_item.assert_called_once()


def test_lambda_missing_field():
    event = {
        "body": json.dumps({
            "tags": ["heron"]
        })
    }

    response = lambda_handler(event, DummyContext())

    assert response["statusCode"] == 400


def test_lambda_invalid_tags():
    event = {
        "body": json.dumps({
            "image_id": "img123.jpg",
            "tags": "not-a-list"
        })
    }

    response = lambda_handler(event, DummyContext())

    assert response["statusCode"] == 400
