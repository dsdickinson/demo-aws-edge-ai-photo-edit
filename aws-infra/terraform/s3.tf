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
    queue_arn = aws_sqs_queue.image_jobs.arn
    events    = ["s3:ObjectCreated:*"]

    filter_suffix = ".jpg"
  }

  depends_on = [
    aws_sqs_queue_policy.allow_s3
  ]
}
