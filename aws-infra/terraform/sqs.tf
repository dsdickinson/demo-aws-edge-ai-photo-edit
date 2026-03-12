resource "aws_sqs_queue" "image_jobs" {
  name                      = "${var.project_name}-queue"
  visibility_timeout_seconds = 60
}

resource "aws_sqs_queue_policy" "allow_s3" {
  queue_url = aws_sqs_queue.image_jobs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid = "AllowS3SendMessage"
      Effect = "Allow"

      Principal = {
        Service = "s3.amazonaws.com"
      }

      Action = "sqs:SendMessage"
      Resource = aws_sqs_queue.image_jobs.arn

      Condition = {
        ArnEquals = {
          "aws:SourceArn" = aws_s3_bucket.raw_images.arn
        }
      }
    }]
  })
}
