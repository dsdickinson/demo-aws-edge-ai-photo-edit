resource "aws_s3_bucket" "raw_images" {
  bucket = "${var.project_name}-raw-images"

  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.raw_images.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_notification" "photo_upload_event" {
  bucket = aws_s3_bucket.raw_images.id

  queue {
    queue_arn = "arn:aws:sqs:us-east-1:015283627155:edge-ai-phedit-demo-queue"
    events    = ["s3:ObjectCreated:*"]

    filter_suffix = ".jpg"
  }

  depends_on = [
    aws_sqs_queue_policy.allow_s3
  ]
}
